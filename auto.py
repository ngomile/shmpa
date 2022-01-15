config = {
    'dam': {
        'names': [
            'tag', 'comment', 'code', 'farmer_name', 'cow_no', 'established',
            'mbg', 'village', 'zone', 'date_recv', 'repaid', 'calves_due',
            'tag_2019', 'date_2019', 'tag_2020', 'date_2020', 'tag_2021',
            'date_2021', 'events', 'breed', 'semen', 'date_born', 'source',
            'date_died', 'cause', 'destination', 'future_decision',
            'last_calved', 'status'
        ],
        'usecols': [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 63, 64, 67, 68, 71, 72, 75,
            79, 80, 81, 82, 85, 86, 87, 88, 89, 99
        ],
    },
    'heifer': {
        'names': [
            'tag', 'farmer_name', 'breed', 'dam', 'events', 'mbg', 'cow_no',
            'repaid', 'transfer_name', 'transfer_mbg', 'transfer_date', 'born',
            'weight', 'monthy_gain', 'last_weighed', 'status'
        ],
        'usecols': [
            1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18
        ],
    },
    'tm': {
        'path': 'C:/Users/SHMPA Data/Documents/shmpa/fmrs TM Jul21.xlsx',
        'sheets': {
            'bt': {
                'heifer_sheet': 'bth',
            },
            'cm': {
                'heifer_sheet': 'cmh',
            },
            'mpA': {
                'heifer_sheet': 'mpAh',
            },
            'mpT': {
                'heifer_sheet': 'mpTh',
            },
            'ck': {
                'heifer_sheet': 'ckh',
            },
        }
    }
}
