import pandas as pd

from config import get_config
from records import RowRecord
from utils import take_cols


class SheetHandler:
    def __init__(self, document: str, sheet: str) -> None:
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

    def yield_as_record(self):
        '''
        Is a generator that yields the rows of both the dam sheet and the heifer sheet
        as a RowRecord
        '''
        for _, row in take_cols(self.df_dams).iterrows():
            yield row

        for _, row in take_cols(self.df_heifers).iterrows():
            yield row
