from typing import Any, Dict, List, NoReturn
from numpy import dtype

import pandas as pd
from bs4 import BeautifulSoup


EXCEL_SHEET: str = 'C:/Users/SHMPA Data/Documents/TM Tags.xlsx'
OUTPUT_DIR: str = 'C:/Users/SHMPA Data/Documents/SHMPA Auto'
MPA_HTML: str = 'C:/Users/SHMPA Data/Downloads/mpa_list.html'
MPT_HTML: str = 'C:/Users/SHMPA Data/Downloads/mpt_list.html'


def soupify_path(path: str) -> BeautifulSoup:
    """
    Open the path to the file and read it into the Beautiful constructor and
    return the result

    :param path
        The path to the excel document
    """
    with open(path, 'r') as f:
        return BeautifulSoup(f.read(), 'html.parser')


def extract_db_tags(soup: BeautifulSoup) -> List[str]:
    """
    Extract the tags from the soupified html document and return a list of
    the tags that are in the table matching the selector tr>td:nth-child(2)

    :param soup
        The soupified html document to retrieve tags from
    """
    return [tag.get_text(strip=True) for tag in soup.select('tr td:nth-child(2)')]


def extract_sheet_tags(df: pd.DataFrame) -> List[str]:
    """
    Extract the tags from the tags column in the dataframe and return a list
    of the tags

    :param df
        The dataframe containing a tags column to extract tags into a list
        of strings
    """
    return [tag for tag in df['tags']] if 'tags' in df.columns else []


def diff_loans(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a dataframe containing the farmers whose loan balances between the
    last and recently calculated quarters, has a non zero balance

    :param df
        The dataframe to compare the values of loans between the last recorded
        entries and the most recent recordings
    """


def db_find_missing(sheet_df: pd.DataFrame, db_tags: List[str] = []) -> pd.DataFrame:
    '''
    Returns a data frame containing rows of values where the tag column in the
    dataframe has tags that have not been put into the database yet

    :param sheet_df
        The dataframe that may be containing tags that have not yet been added to the
        database
    :param db_tags
        The list of tags that are currently contained in the database
    '''
    return sheet_df[[tag not in db_tags for tag in sheet_df['tags']]]


def db_find_removed(sheet_tags: List[str], db_tags: List[str] = []) -> pd.DataFrame:
    '''
    Return a dataframe containing a column of the tags that are in the database but are no
    longer being found in the sheets

    :param sheet_tags
        The list of all the known tags from the sheets that are existing
    :param db_tags
        The list of the last known added tags in the database
    '''
    removed = {'tags': []}
    for tag in db_tags:
        if tag not in sheet_tags:
            removed['tags'].append(tag)
    return pd.DataFrame(removed)


def sheet_to_df(path: str, **kargs) -> pd.DataFrame:
    '''
    Given a path to an excel sheet, convert the sheet into a dataframe and use
    kargs to pass any extra arguments to pd.re

    :param path
        The path to the excel document to turn into a dataframe
    :param kargs
        Extra arguments to pass to the call to pd.read_excel
    '''
    return pd.read_excel(path, **kargs)


def run() -> NoReturn:
    soup = soupify_path(MPA_HTML)
    df = sheet_to_df(
        EXCEL_SHEET,
        dtype={
            'tags': str,
            'events': str
        },
        keep_default_na=False
    )
    sheet_tags = extract_sheet_tags(df)
    db_tags = extract_db_tags(soup)

    missing_tags: pd.DataFrame = db_find_missing(df, db_tags)
    removed_tags = db_find_removed(sheet_tags, db_tags)


if __name__ == '__main__':
    run()
