import pandas as pd

from config import get_config
from records import RowRecord
from utils import take_cols, filter_alive


class SheetHandler:
    def __init__(self, document: str, sheet: str, alive_only: bool = True) -> None:
        config = get_config()
        path = config[document]['path']
        sheets = config[document]['sheets']

        dam_names = config['dam']['names']
        dam_converters = config['dam']['converters']
        dam_cols = config['dam']['cols']

        heifer_names = config['heifer']['names']
        heifer_sheet = config[document]['sheets'][sheet]['heifer_sheet']
        heifer_converters = config['heifer']['converters']

        # In some cases some heifer sheets may have distinct column arrangement
        heifer_cols = config['heifer']['cols']
        heifer_cols = sheets.get(sheet).get('heifer_cols') or heifer_cols

        self.df_dams: pd.DataFrame = pd.read_excel(
            path,
            names=dam_names,
            usecols=dam_cols,
            na_filter=False,
            converters=dam_converters,
            sheet_name=sheet,
            skiprows=2
        )

        self.df_heifers: pd.DataFrame = pd.read_excel(
            path,
            names=heifer_names,
            usecols=heifer_cols,
            converters=heifer_converters,
            sheet_name=heifer_sheet,
            na_filter=False,
            skiprows=3
        )

        if alive_only:
            self.df_dams = filter_alive(self.df_dams)
            self.df_heifers = filter_alive(self.df_heifers)

    def yield_as_record(self):
        '''
        Is a generator that yields the rows of both the dam sheet and the heifer sheet
        as a RowRecord
        '''
        cols = ['tag', 'farmer_name', 'mbg']
        for _, row in take_cols(self.df_dams, cols).iterrows():
            yield RowRecord.from_row(row)

        for _, row in take_cols(self.df_heifers, cols).iterrows():
            yield RowRecord.from_row(row)
