if __name__ == '__main__':
    import time

    import pandas as pd

    from auto import SheetHandler
    from utils import OUTPUT_DIR

    start = time.perf_counter()
    document = 'tm'
    transferred: bool = False

    if transferred:
        sheets = ['mpA', 'mpT']
        transfers = list(SheetHandler.find_all_transfers(document, sheets))
        _path = f'{OUTPUT_DIR}/transfers.xlsx'
        pd.DataFrame(transfers).to_excel(_path, index=False)

    end = time.perf_counter()
    print(f'That took {end - start}')
