from typing import List, NoReturn

import pandas as pd
from bs4 import BeautifulSoup


def try_parse_int(s: str, base=10, val=0) -> int:
    """
    Given argument string, attempt to parse the string to its integer value
    if exception is thrown. Catch it and return default val
    """
    try:
        return int(s, base)
    except ValueError:
        return val


def soupify_path(path: str) -> BeautifulSoup:
    """
    Open the path to the file and read it into the Beautiful constructor and
    return the result
    """


def extract_web_tags(soup: BeautifulSoup) -> List[str]:
    """
    Extract the tags from the soupified html document and return a list of
    the tags that are in the table matching the selector tr > td:nth-child(2)
    """


def extract_sheet_tags(df: pd.DataFrame) -> List[str]:
    """
    Extract the tags from the tags column in the dataframe and return a list
    of the tags
    """


def diff_loans(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a dataframe containing the farmers whose loan balances between the
    last and recently calculated quarters, has a non zero balance
    """


def run() -> NoReturn:
    pass


if __name__ == '__main__':
    run()
