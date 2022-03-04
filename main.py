import time

import pandas as pd

from auto import SheetHandler
from utils import OUTPUT_DIR


def main():
    start = time.perf_counter()
    document = 'tm'
    transferred: bool = False

    if transferred:
        transfers = list(SheetHandler.find_transferred(document))
        _path = f'{OUTPUT_DIR}/transfers.xlsx'
        pd.DataFrame(transfers).to_excel(_path, index=False)

    end = time.perf_counter()
    print(f'That took {end - start}')


if __name__ == '__main__':
    main()
