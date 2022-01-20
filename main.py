import os
from datetime import date
from typing import List

import pandas as pd
from bs4 import BeautifulSoup


EXCEL_SHEET: str = 'C:/Users/SHMPA Data/Documents/TM Tags.xlsx'
OUTPUT_DIR: str = 'C:/Users/SHMPA Data/Documents/SHMPA Auto'
MPA_HTML: str = 'C:/Users/SHMPA Data/Downloads/mpa_list.html'
MPT_HTML: str = 'C:/Users/SHMPA Data/Downloads/mpt_list.html'

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


def sheet_only_tags(sheet_tags: List[str], db_tags: List[str] = []) -> List[str]:
    '''
    Returns a list of tags that are only appearing in the excel sheets and have
    not been entered in the database yet

    :param sheet_df
        The dataframe that may be containing tags that have not yet been added to the
        database
    :param db_tags
        The list of tags that are currently contained in the database
    '''
    tags: List[str] = []
    for tag in sheet_tags:
        if tag not in db_tags:
            tags.append(tag)

    return tags


def db_only_tags(sheet_tags: List[str], db_tags: List[str] = []) -> List[str]:
    '''
    Returns a list of tags that are only appearing in the database and are not being
    found in the sheets

    :param sheet_tags
        The list of all the known tags from the sheets that are existing
    :param db_tags
        The list of the last known added tags in the database
    '''
    tags: List[str] = []
    for tag in db_tags:
        if tag not in sheet_tags:
            tags.append(tag)
    return tags


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


def run():
    soup = soupify_path(MPA_HTML)
    df = sheet_to_df(
        EXCEL_SHEET,
        dtype={
            'tags': str,
            'events': str
        },
        keep_default_na=False
    )

    extracted_sheet = extract_sheet_tags(df)
    extracted_db = extract_db_tags(soup)

    sheet_tags = sheet_only_tags(extracted_sheet, extracted_db)
    db_tags = db_only_tags(extracted_sheet, extracted_db)

    df_sheet = df[[tag in sheet_tags for tag in df['tags']]]
    df_db = pd.DataFrame({'tags': sorted(db_tags)})

    unique_tags = tuple((tag[1] for tag in df['tags'].iteritems()))
    tag_count = len(unique_tags)

    print(f'Found {tag_count} unique tags')

    if os.path.isfile(SHEET_ONLY_PATH):
        os.remove(SHEET_ONLY_PATH)

    if os.path.isfile(DB_ONLY_PATH):
        os.remove(DB_ONLY_PATH)

    df_sheet.to_excel(SHEET_ONLY_PATH, index=False)
    df_db.to_excel(DB_ONLY_PATH, index=False)


if __name__ == '__main__':
    import pandas as pd
    from config import get_config

    config = get_config()
    document = 'tm'

    dam_names = config['dam']['names']
    dam_cols = config['dam']['cols']
    dam_converters = config['dam']['converters']
    dam_sheet = 'mpA'

    path = config[document]['path']

    heifer_names = config['heifer']['names']
    heifer_cols = config['heifer']['cols']
    heifer_converters = config['heifer']['converters']
    heifer_sheet = config[document]['sheets'][dam_sheet]['heifer_sheet']

    df_dams = pd.read_excel(
        path,
        names=dam_names,
        usecols=dam_cols,
        na_filter=False,
        converters=dam_converters,
        sheet_name=dam_sheet,
        skiprows=2
    )

    df_heifers = pd.read_excel(
        path,
        names=heifer_names,
        usecols=heifer_cols,
        converters=heifer_converters,
        sheet_name=heifer_sheet,
        na_filter=False,
    )
