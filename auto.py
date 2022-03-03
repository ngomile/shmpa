from typing import List, Any, Union
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
        list_of_years: list[int] = sorted(list(years_entry.keys()))

        path_check = ['path' in years_entry[year] for year in list_of_years]
        assert all(path_check), 'Path to file not provided'

        path: str = ''
        if year:
            # Year has been provided, make sure it is in list_of_years
            assert year in list_of_years, f'Provided year {year} not in {list_of_years}'
            path = years_entry[year]['path']
        else:
            # In situations where year is not specified, fallback to using the most recent document
            year = list_of_years[-1]
            path = years_entry[year]['path']

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
        self._YEAR = year

        custom_names: Union[list[str], None] = None
        custom_cols: Union[str, None] = None

        if year and (dam := years_entry[year].get('dam', None)):
            custom_names = dam['names']
            custom_cols = dam['cols']

        self._DAM_NAMES: list[str] = custom_names or config['dam']['names']
        self._DAM_COLS: str = custom_cols or config['dam']['cols']
        self._DAM_CONVERTERS: dict[str, Any] = config['dam']['converters']

        self._HEIFER_NAMES: list[str] = config['heifer']['names']
        self._HEIFER_COLS: str = config['heifer']['cols']
        self._HEIFER_CONVERTERS: dict[str,
                                      Any] = config['heifer']['converters']

    @ property
    def df_dams(self) -> pd.DataFrame:
        if not hasattr(self, '_DF_DAMS'):
            self._DF_DAMS: pd.DataFrame = pd.read_excel(
                self._PATH,
                names=self._DAM_NAMES,
                usecols=self._DAM_COLS,
                na_filter=False,
                converters=self._DAM_CONVERTERS,
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
            document = self._CONFIG['documents'][self._DOCUMENT]
            sheets: dict[str, dict[str, str]] = document['sheets']
            heifer_sheet = sheets[self._SHEET].get('heifer_sheet')

            if heifer_sheet:
                # In some cases some heifer sheets may have distinct column arrangement
                custom_names = None
                custom_cols = None
                year_entry = document['years'][self._YEAR]
                custom_heifer_attrs = year_entry.get('heifer')

                if custom_heifer_attrs:
                    custom_names = custom_heifer_attrs['names']
                    custom_cols = custom_heifer_attrs['cols']

                self._DF_HEIFERS = pd.read_excel(
                    self._PATH,
                    names=custom_names or self._HEIFER_NAMES,
                    usecols=custom_cols or self._HEIFER_COLS,
                    converters=self._HEIFER_CONVERTERS,
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

    @classmethod
    def find_transferred(cls, document: str):
        '''
        Iterate through web animal list and find animals whose herds do not match with
        the excel entries for that animal
        '''
        records = cls.yield_all_records()
        sheet_records = {record.tag: record for record in records}

        for db_animal in stream_db_animals(document):
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

    def search(self, tag: str = '', farmer_name: str = '') -> pd.DataFrame:
        '''
        Filters out the dataframe by checking the values provided against it,
        when a match is found the dataframe is reassigned the result of the
        comparison check. And the final filtered dataframe is returned

        :param tag
            The tag to search for through the tag column
        :param farmer_name
            The farmer name to search for through the farmer_name column
        '''

        records_list: list[dict] = [record.to_dict()
                                    for record in self.yield_records()]
        dataframe = pd.DataFrame(records_list)

        if tag:
            dataframe = dataframe[dataframe['tag'].str.contains(tag)]

        if farmer_name:
            dataframe = dataframe[dataframe['farmer_name'].str.contains(
                farmer_name)]

        return dataframe.reset_index(drop=True)

    def search_name(self, farmer_name: str) -> pd.DataFrame:
        '''
        Helper method to search only for farmers that happen to have a
        matching name

        :param farmer_name
            The name of the farmer to search for
        '''
        return self.search(farmer_name=farmer_name)

    def search_tag(self, tag: str) -> pd.DataFrame:
        '''
        Helper method to help search dataframe where the farmer_name column
        happens to match with teh searched tag

        :param tag
            The tag of the cow to search for
        '''
        return self.search(tag=tag)

    def compare_to_db(self):
        '''
        Finds records that are only appearing in the database and also only
        appearing in the sheets and yields a dictionary containing the herd
        name and the location of where it is being found
        '''
        db_animal = stream_db_animals(self._DOCUMENT, self._SHEET)
        sheet_records = self.yield_records()

        db_entries = {entry.tag: entry for entry in db_animal}
        sheet_entries = {entry.tag: entry for entry in sheet_records}

        for db_entry in db_entries.keys():
            if db_entry not in sheet_entries:
                entry = db_entries[db_entry]

                yield {
                    'tag': entry.tag,
                    'herd': entry.herd,
                    'location': 'DB_ONLY'
                }

        for sheet_entry in sheet_entries.keys():
            if sheet_entry not in db_entries:
                entry = sheet_entries[sheet_entry]

                yield {
                    'tag': entry.tag,
                    'herd': entry.farmer_name,
                    'location': 'SHEET_ONLY'
                }

    @classmethod
    def compare_all_db(cls, document: str):
        '''
        Similar to compare_with_db but is now able to process all the documents and
        their respective sheets and yields any differences between the two after checking
        for entries that are not found in either one of the records
        '''
        db_animal = stream_db_animals(document)
        sheet_records = cls.yield_all_records()

        db_entries = {entry.tag: entry for entry in db_animal}
        sheet_entries = {entry.tag: entry for entry in sheet_records}

        for db_entry in db_entries.keys():
            if db_entry not in sheet_entries:
                entry = db_entries[db_entry]

                yield {
                    'tag': entry.tag,
                    'herd': entry.herd,
                    'location': 'DB_ONLY'
                }

        for sheet_entry in sheet_entries.keys():
            if sheet_entry not in db_entries:
                entry = sheet_entries[sheet_entry]

                yield {
                    'tag': entry.tag,
                    'herd': entry.farmer_name,
                    'location': 'SHEET_ONLY'
                }

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
        for _, row in cls.yield_all_rows(alive):
            yield RowRecord.from_row(row)


if __name__ == '__main__':
    import time

    start = time.perf_counter()

    config = get_config()
    for document in config['documents'].keys():
        sheets = config['documents'][document]['sheets']
        years = config['documents'][document]['years']
        for year in sorted(list(years.keys())):
            for sheet in sheets.keys():
                sh = SheetHandler(document, sheet=sheet, year=year)
                print(sh.df_dams)
                print(sh.df_heifers)

    end = time.perf_counter()
    print(f'That took {end - start}')
