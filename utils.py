import pandas as pd
from typing import List


def take_cols(df: pd.DataFrame, cols: List[str] = ['tag', 'farmer_name']) -> pd.DataFrame:
    '''
    Utility function to return a dataframe of only the selected columns
    :param df
        The dataframe containing rows of interest
    :param cols
        The list of column names to only show for the returned dataframe
    '''
    return df[cols]
