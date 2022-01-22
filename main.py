if __name__ == '__main__':
    import time

    from auto import SheetHandler

    start = time.perf_counter()
    document = 'tm'
    sheet = 'mpT'

    sheet_handler = SheetHandler(document, sheet)
    df_dams = sheet_handler.df_dams
    df_heifers = sheet_handler.df_heifers

    end = time.perf_counter()
    print(f'That took {end - start}')
