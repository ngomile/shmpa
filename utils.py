import os
from datetime import date
import re
from typing import List

from bs4 import BeautifulSoup
import pandas as pd

from config import get_config
from records import DBRecord

OUTPUT_DIR: str = 'C:/Users/SHMPA Data/Documents/SHMPA Auto'

DATE_TIME: str = date.today().strftime('%d_%m_%Y')

SHEET_ONLY_PATH: str = os.path.join(
    OUTPUT_DIR,
    f'SHEET_TAGS_{DATE_TIME}.xlsx'
)
DB_ONLY_PATH: str = os.path.join(OUTPUT_DIR, f'DB_TAGS_{DATE_TIME}.xlsx')


def soupify_path(path: str) -> BeautifulSoup:
    """
    Open the path to the file and read it into the Beautiful constructor and
    return the result

    :param path
        The path to the excel document
    """
    with open(path, 'rb') as f:
        return BeautifulSoup(f, 'html.parser')


def soupify_web(document: str, sheet: str = None):
    '''
    Given document as key to one of the sheets in config, find all sheets that have
    a website entry for the document and yield the soup instance

    :param document:
        The key of the document to be used
    :param sheet:
        If specified, use only the file associated with this sheet
    '''
    config = get_config()
    sheets = config['documents'][document]['sheets']

    for sheet_key in sheets.keys():
        if sheet and sheet_key != sheet:
            continue

        if db_path := sheets[sheet_key].get('db_path'):
            assert os.path.isfile(
                db_path
            ), 'Incorrect path provided for database file'
            yield soupify_path(db_path)


def stream_db_animals(document: str, sheet: str = None):
    '''
    Returns an iterable of all the animals in the database in separate lists as one
    stream of values to be consumed

    :param document:
        The key of the document to scan for paths to web documents
    '''
    herd_selector = 'tr td:nth-child(1)'
    tag_selector = 'tr td:nth-child(2)'
    herd_name = ''

    for soup in soupify_web(document, sheet):
        for herd, tag in zip(soup.select(herd_selector), soup.select(tag_selector)):
            herd, tag = herd.get_text(strip=True), tag.get_text(strip=True)
            if herd:
                herd_name = herd

            yield DBRecord(tag, herd_name)


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
