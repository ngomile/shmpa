import re
from typing import List

import pandas as pd


def take_cols(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    '''
    Utility function to return a dataframe of only the selected columns
    :param df
        The dataframe containing rows of interest
    :param cols
        The list of column names to only show for the returned dataframe
    '''
    return df[cols]


def filter_alive(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Finds cows that match the regular expression of digits only, assumes
    that number only tags are cows that are alive

    :param df
        The dataframe to filter rows for cows that are alive only
    '''
    return df[df['tag'].str.contains(
        '^\d+$',
        regex=True,
        flags=re.I
    )].reset_index(drop=True)
