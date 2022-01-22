if __name__ == '__main__':
    import time

    from auto import SheetHandler

    start = time.perf_counter()
    document = 'tm'
    sheets = ['mpA', 'mpT']
    transfers = []

    for sheet in sheets:
        sheet_handler = SheetHandler(document, sheet)
        df_dams = sheet_handler.df_dams
        df_heifers = sheet_handler.df_heifers

        for transfer in sheet_handler.find_transferred():
            transfers.append(transfer)

    print(transfers)
    end = time.perf_counter()
    print(f'That took {end - start}')
