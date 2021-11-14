from typing import Any, Dict, List, NoReturn

import pandas as pd
from bs4 import BeautifulSoup


EXCEL_SHEET: str = ''
MPA_HTML: str = 'C:/Users/SHMPA Data/Downloads/mpa_list.html'
MPT_HTML: str = 'C:/Users/SHMPA Data/Downloads/mpt_list.html'


def soupify_path(path: str) -> BeautifulSoup:
    """
    Open the path to the file and read it into the Beautiful constructor and
    return the result
    """
    with open(path, 'r') as f:
        return BeautifulSoup(f.read(), 'html.parser')


def extract_web_tags(soup: BeautifulSoup) -> List[str]:
    """
    Extract the tags from the soupified html document and return a list of
    the tags that are in the table matching the selector tr>td:nth-child(2)
    """
    return [tag.get_text(strip=True) for tag in soup.select('tr td:nth-child(2)')]


def extract_sheet_tags(df: pd.DataFrame) -> List[str]:
    """
    Extract the tags from the tags column in the dataframe and return a list
    of the tags
    """
    return [tag for tag in df['tags']] if 'tags' in df.columns else []


def diff_loans(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a dataframe containing the farmers whose loan balances between the
    last and recently calculated quarters, has a non zero balance
    """


def find(query: Dict[str, Any]) -> pd.DataFrame:
    """
    Given the query, filter all the rows in the dataframe and match the ones that
    fulfill the query criteria
    """


def db_find_missing(sheet_df: pd.DataFrame, db_tags: List[str] = []) -> pd.DataFrame:
    '''
    Returns a data frame containing rows of values where the tag column in the
    dataframe has tags that have not been put into the database yet
    '''


def sheet_find_removed(sheet_tags: List[str], db_tags: List[str] = []) -> List[str]:
    '''
    Return a list of the tags that are in the database but are no longer being
    found in the sheets
    '''


def run() -> NoReturn:
    pass


if __name__ == '__main__':
    run()
