from typing import Any

DAM_COLS = {
    'tag': 'B',
    'comment': 'C',
    'code': 'D',
    'farmer_name': 'E',
    'cow_no': 'F',
    'established': 'G',
    'mbg': 'H',
    'village': 'J',
    'zone': 'K',
    'date_recv': 'L',
    'repaid': ' M',
    'calves_due': 'N',
    'tag_2019': 'BM',
    'date_2019': 'BN',
    'tag_2020': 'BQ',
    'date_2020': 'BR',
    'tag_2021': 'BU',
    'date_2021': 'BV',
    'events': 'BY',
    'breed': 'CC',
    'semen': 'CD',
    'born': 'CE',
    'source': 'CF',
    'date_removed': 'CS',
    'cause': 'CT',
    'destination': 'CU',
    'future_decision': 'CV',
    'last_calved': 'CW',
    'status': 'CZ',
}

HEIFER_COLS = {
    'tag': 'B',
    'code': 'C',
    'farmer_name': 'D',
    'breed': 'E',
    'semen': 'F',
    'dam': 'I',
    'events': 'J',
    'mbg': 'K',
    'cow_no': 'L',
    'repaid': 'M',
    'destination': 'N',
    'transfer_mbg': 'O',
    'date_removed': 'P',
    'born': 'Q',
    'weight': 'R',
    'monthy_gain': 'S',
    'last_weighed': 'T',
    'status': 'U',
}


def get_config() -> dict[str, dict[str, Any]]:
    return {
        'dam': {
            'names': [name for name in DAM_COLS.keys()],
            'cols': [col for col in DAM_COLS.values()],
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
                'tag', 'code', 'farmer_name', 'breed', 'dam', 'events', 'mbg', 'cow_no',
                'repaid', 'transfer_name', 'transfer_mbg', 'transfer_date', 'born',
                'weight', 'monthy_gain', 'last_weighed', 'status',
            ],
            'cols': [1, 2, 3, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, ],
            'converters': {
                'tag': str,
                'dam': str,
                'monthly_gain': int,
                'repaid': bool,
            }
        },
        'documents': {
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
                        'db_path': 'C:/Users/SHMPA Data/Documents/mpa.html'
                    },
                    'mpT': {
                        'heifer_sheet': 'mpTh',
                        'db_path': 'C:/Users/SHMPA Data/Documents/mpt.html'
                    },
                }
            }

        }
    }
