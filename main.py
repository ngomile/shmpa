from typing import Any, Dict, List, NoReturn

import pandas as pd
from bs4 import BeautifulSoup


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


def find(query: Dict[str, Any]) -> pd.DataFrame:
    """
    Given the query, filter all the rows in the dataframe and match the ones that
    fulfill the query criteria
    """


def run() -> NoReturn:
    pass


if __name__ == '__main__':
    run()
