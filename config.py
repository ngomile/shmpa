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
    'removed': 'CS',
    'cause': 'CT',
    'destination': 'CU',
    'decision': 'CV',
    'last_calved': 'CW',
    'status': 'CZ',
}


def get_config() -> dict[str, dict[str, Any]]:
    return {
        'dam': {
            'names': [
                'tag', 'comment', 'code', 'farmer_name', 'cow_no', 'established',
                'mbg', 'village', 'zone', 'date_recv', 'repaid', 'calves_due',
                'tag_2019', 'date_2019', 'tag_2020', 'date_2020', 'tag_2021',
                'date_2021', 'events', 'breed', 'semen', 'born', 'source',
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
