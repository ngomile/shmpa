from typing import Any


def get_config() -> dict[str, dict[str, Any]]:
    return {
        'dam': {
            'names': [
                'tag', 'comment', 'code', 'farmer_name', 'cow_no', 'established',
                'mbg', 'village', 'zone', 'date_recv', 'repaid', 'calves_due',
                'tag_2019', 'date_2019', 'tag_2020', 'date_2020', 'tag_2021',
                'date_2021', 'events', 'breed', 'semen', 'date_born', 'source',
                'date_removed', 'cause', 'destination', 'future_decision',
                'last_calved', 'status',
            ],
            'cols': [
                1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 64, 65, 68, 69, 72, 73, 76,
                80, 81, 82, 83, 96, 97, 98, 99, 100, 110,
            ],
            'converters': {
                'tag': str,
                'code': str,
                'cow_no': str,
                'established': str,
                'zone': str,
                'repaid': bool,
            }
        },
        'heifer': {
            'names': [
                'tag', 'farmer_name', 'breed', 'dam', 'events', 'mbg', 'cow_no',
                'repaid', 'transfer_name', 'transfer_mbg', 'transfer_date', 'born',
                'weight', 'monthy_gain', 'last_weighed', 'status',
            ],
            'cols': [1, 3, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, ],
            'converters': {
                'tag': str,
                'dam': str,
                'monthly_gain': int,
                'repaid': bool,
            }
        },
        'tm': {
            'path': 'C:/Users/SHMPA Data/Documents/shmpa/fmrs TM Jul21.xlsx',
            'sheets': {
                'bt': {
                    'heifer_sheet': 'bth',
                    'heifer_cols': [1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, ]
                },
                'cm': {
                    'heifer_sheet': 'cmh',
                },
                'mpA': {
                    'heifer_sheet': 'mpAh',
                    'db_path': 'C:/Users/SHMPA Data/Documents/mpa_animals.html'
                },
                'mpT': {
                    'heifer_sheet': 'mpTh',
                    'db_path': 'C:/Users/SHMPA Data/Documents/mpt_animals.html'
                },
            }
        }
    }
