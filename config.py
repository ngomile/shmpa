from ntpath import join
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
    'repaid': 'M',
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
    'monthly_gain': 'S',
    'last_weighed': 'T',
    'status': 'U',
}

DAM_COLS_22 = {
    'tag': 'B',
    'comment': 'C',
    'farmer_name': 'D',
    'cow_no': 'E',
    'established': 'F',
    'mbg': 'G',
    'village': 'I',
    'zone': 'J',
    'date_recv': 'K',
    'repaid': 'L',
    'calves_due': 'M',
    'tag_2019': 'BL',
    'date_2019': 'BM',
    'tag_2020': 'BP',
    'date_2020': 'BQ',
    'tag_2021': 'BT',
    'date_2021': 'BU',
    'events': 'CB',
    'breed': 'CF',
    'semen': 'CG',
    'born': 'CH',
    'source': 'CI',
    'date_removed': 'CV',
    'cause': 'CW',
    'destination': 'CX',
    'future_decision': 'CY',
    'last_calved': 'CZ',
    'months_open': 'DB',
    'status': 'DC',
    'equipment_loan': 'DE',
}

NO_CODE_HEIFER_COLS = {
    'tag': 'B',
    'farmer_name': 'C',
    'breed': 'D',
    'semen': 'E',
    'dam': 'J',
    'events': 'K',
    'mbg': 'L',
    'cow_no': 'M',
    'repaid': 'N',
    'destination': 'O',
    'transfer_mbg': 'P',
    'date_removed': 'Q',
    'born': 'R',
    'weight': 'S',
    'monthly_gain': 'T',
    'last_weighed': 'U',
    'status': 'V',
}


def get_config() -> dict[str, dict[str, Any]]:
    DAM_NAMES = [name for name in DAM_COLS.keys()]
    DAM_NAMES_22 = [name for name in DAM_COLS_22.keys()]
    HEIFER_NAMES = [name for name in HEIFER_COLS.keys()]
    NO_CODE_HEIFER_NAMES = [name for name in NO_CODE_HEIFER_COLS.keys()]

    return {
        'dam': {
            'names': DAM_NAMES,
            'cols': ', '.join([DAM_COLS[col] for col in DAM_NAMES]),
            'converters': {
                'tag': str,
                'farmer_name': str,
                'code': str,
                'cow_no': str,
                'established': int,
                'zone': str,
                'repaid': bool,
                'born': str,
                'date_removed': str,
                'breed': str,
            }
        },
        'heifer': {
            'names': HEIFER_NAMES,
            'cols': ', '.join([HEIFER_COLS[col] for col in HEIFER_NAMES]),
            'converters': {
                'tag': str,
                'farmer_name': str,
                'dam': str,
                'repaid': bool,
                'born': str,
                'date_removed': str,
                'breed': str,
            }
        },
        'documents': {
            'tm': {
                'years': {
                    2021: {
                        'path': 'C:/Users/SHMPA Data/Documents/shmpa/fmrs TM Jul21.xlsx',
                        'has_code': True,
                    },
                    2022: {
                        'path': 'C:/Users/SHMPA Data/Documents/shmpa/fmrs TM Jan22.xlsx',
                        'dam': {
                            'names': DAM_NAMES_22,
                            'cols': ', '.join([DAM_COLS_22[col] for col in DAM_NAMES_22]),
                        },
                        'heifer': {
                            'names': NO_CODE_HEIFER_NAMES,
                            'cols': ', '.join([NO_CODE_HEIFER_COLS[col] for col in NO_CODE_HEIFER_NAMES]),
                        },
                    },
                },
                'sheets': {
                    # 'cm': {
                    #     'heifer_sheet': 'cmh',
                    # },
                    'mpA': {
                        'heifer_sheet': 'mpAh',
                        'db_path': 'C:/Users/SHMPA Data/Documents/mpa.html',
                    },
                    'mpT': {
                        'heifer_sheet': 'mpTh',
                        'db_path': 'C:/Users/SHMPA Data/Documents/mpt.html',
                    },
                },
            },
        },
    }


if __name__ == '__main__':
    from pprint import PrettyPrinter

    PrettyPrinter(compact=True, sort_dicts=True).pprint(get_config())
