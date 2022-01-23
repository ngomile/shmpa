from typing import List

import pandas as pd

from config import get_config
from records import RowRecord
from utils import take_cols, filter_alive, stream_db_animals


class SheetHandler:
    def __init__(self, document: str, sheet: str, alive_only: bool = True) -> None:
        self._config = get_config()
        self._path = self._config['documents'][document]['path']
        self._alive_only = alive_only
        self._document = document
        self._sheet = sheet

    @property
    def df_dams(self) -> pd.DataFrame:
        if not hasattr(self, '_df_dams'):
            dam_names = self._config['dam']['names']
            dam_converters = self._config['dam']['converters']
            dam_cols = self._config['dam']['cols']

            self._df_dams: pd.DataFrame = pd.read_excel(
                self._path,
                names=dam_names,
                usecols=dam_cols,
                na_filter=False,
                converters=dam_converters,
                sheet_name=self._sheet,
                skiprows=2
            )

            if self._alive_only:
                self._df_dams = filter_alive(self._df_dams)

        return self._df_dams

    @property
    def df_heifers(self) -> pd.DataFrame:
        if not hasattr(self, '_df_heifers'):
            heifer_names = self._config['heifer']['names']
            heifer_sheet = self._config['documents'][self._document]['sheets'][self._sheet]['heifer_sheet']
            heifer_converters = self._config['heifer']['converters']

            # In some cases some heifer sheets may have distinct column arrangement
            sheets = self._config['documents'][self._document]['sheets']
            heifer_cols = self._config['heifer']['cols']
            heifer_cols = sheets.get(self._sheet).get(
                'heifer_cols') or heifer_cols

            self._df_heifers: pd.DataFrame = pd.read_excel(
                self._path,
                names=heifer_names,
                usecols=heifer_cols,
                converters=heifer_converters,
                sheet_name=heifer_sheet,
                na_filter=False,
                skiprows=3
            )

            if self._alive_only:
                self._df_heifers = filter_alive(self._df_heifers)

        return self._df_heifers

    def yield_rows(self):
        '''
        Lazily returns the rows for all the dam and heifer sheets
        '''
        cols = ['tag', 'farmer_name', 'mbg']
        for entry in take_cols(self.df_dams, cols).iterrows():
            yield entry

        for entry in take_cols(self.df_heifers, cols).iterrows():
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
        records = self.yield_records()
        owners = {record.tag: record for record in records}

        for entry in stream_db_animals(self._document):
            _from = entry.herd.lower()
            if entry.tag in owners and _from != owners[entry.tag].farmer_name.lower():
                yield {
                    'tag': entry.tag,
                    'from': entry.herd,
                    'to': owners[entry.tag].farmer_name,
                    'transfer_farm_code': '',
                    'transfer_mbg': owners[entry.tag].mbg,
                    'date': '',
                    'reason': ''
                }

    @classmethod
    def find_all_transfers(cls, document: str, sheets: List[str]):
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
            sheet_handler = cls(document, sheet)
            for transfer in sheet_handler.find_transferred():
                yield transfer
