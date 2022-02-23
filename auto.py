from typing import List
import os

import pandas as pd

from config import get_config
from records import RowRecord
from utils import filter_alive, stream_db_animals


class SheetHandler:
    _CONFIG = get_config()

    def __init__(self, document: str, /, sheet: str = None, alive_only: bool = True, year: int = None) -> None:
        config = self._CONFIG
        documents = config['documents']

        assert document in documents, f'Incorrect document key provided {document}'
        document_entry = documents[document]
        assert 'years' in document_entry, f'Years entry not applied for {document} document'

        years_entry = document_entry['years']
        # Extract all list of years associated with the provided document
        list_of_years = sorted(list(years_entry.keys()))

        path_check = ['path' in years_entry[year] for year in list_of_years]
        assert all(path_check), 'Path to file not provided'

        path = ''
        if year:
            # Year has been provided, make sure it is in list_of_years
            assert year in list_of_years, f'Provided year {year} not in {list_of_years}'
            path = years_entry[year]['path']
        else:
            # In situations where year is not specified, fallback to using the most recent document
            recent = list_of_years[-1]
            path = years_entry[recent]['path']

        error_msg = f'Incorrect file path provided {path}'
        assert os.path.isfile(path), error_msg

        if sheet:
            error_msg = f'Incorrect key for sheet {sheet}'
            assert sheet in document_entry['sheets'], error_msg
        elif sheet is None:
            entries = document_entry['sheets'].keys()
            sheet = list(entries)[0]

        self._PATH: str = path
        self._ALIVE_ONLY = alive_only
        self._DOCUMENT = document
        self._SHEET = sheet

    @ property
    def df_dams(self) -> pd.DataFrame:
        if not hasattr(self, '_DF_DAMS'):
            dam_names = self._CONFIG['dam']['names']
            dam_converters = self._CONFIG['dam']['converters']
            dam_cols = self._CONFIG['dam']['cols']

            self._DF_DAMS: pd.DataFrame = pd.read_excel(
                self._PATH,
                names=dam_names,
                usecols=dam_cols,
                na_filter=False,
                converters=dam_converters,
                sheet_name=self._SHEET,
                skiprows=2
            )

            if self._ALIVE_ONLY:
                self._DF_DAMS = filter_alive(self._DF_DAMS)
            self._DF_DAMS['is_dam'] = True

        return self._DF_DAMS

    @property
    def df_heifers(self) -> pd.DataFrame:
        if not hasattr(self, '_DF_HEIFERS'):
            # Initialize heifer df to empty in case heifer sheet is unspecified
            self._DF_HEIFERS: pd.DataFrame = pd.DataFrame({})
            heifer_names = self._CONFIG['heifer']['names']
            heifer_cols = self._CONFIG['heifer']['cols']
            heifer_converters = self._CONFIG['heifer']['converters']

            heifer_sheet = self._CONFIG['documents'][self._DOCUMENT]['sheets'][self._SHEET].get(
                'heifer_sheet'
            )

            if heifer_sheet:
                # In some cases some heifer sheets may have distinct column arrangement
                sheets = self._CONFIG['documents'][self._DOCUMENT]['sheets']
                heifer_cols = sheets.get(self._SHEET).get(
                    'heifer_cols') or heifer_cols

                self._DF_HEIFERS = pd.read_excel(
                    self._PATH,
                    names=heifer_names,
                    usecols=heifer_cols,
                    converters=heifer_converters,
                    sheet_name=heifer_sheet,
                    na_filter=False,
                    skiprows=3
                )

                if self._ALIVE_ONLY:
                    self._DF_HEIFERS = filter_alive(self._DF_HEIFERS)
                self.df_heifers['is_dam'] = False

        return self._DF_HEIFERS

    def yield_rows(self):
        '''
        Lazily returns the rows for all the dam and heifer sheets
        '''
        for entry in self.df_dams.iterrows():
            yield entry

        for entry in self.df_heifers.iterrows():
            yield entry

    def yield_records(self):
        '''
        Lazily creates instances of RowRecords from rows
        '''
        for _, row in self.yield_rows():
            yield RowRecord.from_row(row)

    def find_transferred(self):
        '''
        Iterate through web animal list and find animals whose herds do not match with
        the excel entries for that animal
        '''
        sheet_records = {record.tag: record for record in self.yield_records()}

        for db_animal in stream_db_animals(self._DOCUMENT):
            # _from stores the name of the herd taken from the database and we then
            # compare it's value to the farmer name of the cow tag in the sheets
            db_tag = db_animal.tag
            db_herd = db_animal.herd.lower()

            if db_tag in sheet_records and db_herd != sheet_records[db_tag].farmer_name.lower():
                sheet_record = sheet_records[db_tag]

                yield {
                    'tag': db_tag,
                    'from': ' '.join([name.capitalize() for name in db_herd.split(' ')]),
                    'to': sheet_record.farmer_name,
                    'transfer_farm_code': sheet_record.code,
                    'transfer_mbg': sheet_record.mbg,
                    'date': '',
                    'reason': ''
                }

    @classmethod
    def find_all_transfers(cls, document: str, sheets: List[str], alive: bool = False):
        '''
        This method goes through the provided sheets and creates SheetHandler instances
        for each sheet and finds the cows that have likely been transferred to other
        farmers

        :param document
            The document containing the sheets we are interested in
        :param sheets
            The sheets to scan through and compare animal list from the database to
            them
        '''
        for sheet in sheets:
            sheet_handler = cls(document, sheet, alive)
            for transfer in sheet_handler.find_transferred():
                yield transfer

    @classmethod
    def yield_all_rows(cls, alive: bool = True):
        '''
        Goes through all the documents and creates SheetHandler instances for each
        document and yields the animals for all the dam and heifer sheets in one
        stream of data

        :param alive
            Whether to filter animals that are only alive
        '''
        for document in cls._CONFIG['documents'].keys():
            for sheet in cls._CONFIG['documents'][document]['sheets'].keys():
                for row in SheetHandler(document, sheet, alive).yield_rows():
                    yield row

    @classmethod
    def yield_all_records(cls, alive: bool = True):
        '''
        Creates instances of RowRecords for every row returned from the call to
        yield_all_rows, this is a convenience method as sometimes we might want
        to manipulate commonly held attributes that appear in both the dam and
        heifer sheets

        :param alive
            Whether to only return the rows of animals that are alive
        '''
        for index, row in cls.yield_all_rows(alive):
            yield RowRecord.from_row(row)
