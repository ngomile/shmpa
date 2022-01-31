from dataclasses import dataclass
from typing import Dict, Any

import pandas as pd


@dataclass
class CalvingRecord:
    '''
    This type stores the calving record for a cow, the fields contain the tag
    and date for the calving
    '''
    tag: str
    date: str


@dataclass
class DamRecord:
    '''
    This type stores the fields related to the dam, the fields hold various
    information related to the cow
    '''
    tag: str
    comment: str
    code: str
    farmer_name: str
    cow_no: str
    established: int
    mbg: str
    village: str
    zone: str
    date_recv: str
    repaid: bool
    calves_due: str
    calving_records: Dict[str, CalvingRecord]
    events: str
    breed: str
    semen: str
    born: str
    source: str
    died: str
    cause: str
    destination: str
    future_decision: str
    last_calved: str
    status: str

    @classmethod
    def from_row(cls):
        return DamRecord()


@dataclass
class TransferRecord:
    '''
    This type stores information for a transfer of a cow from one location to
    another
    '''
    name: str
    mbg: str
    date: str


@dataclass
class RemovalRecord:
    '''
    This type stores information related to the removal of a cow from the farm
    because it either died or other reasons
    '''
    date_removed: str
    cause: str
    destination: str
    decision: str


@dataclass
class HeiferRecord:
    '''
    This type stores information of a heifer
    '''
    tag: str
    farmer_name: str
    breed: str
    dam: str
    events: str
    mbg: str
    cow_no: str
    repaid: bool
    transfer: TransferRecord
    born: str
    weight: float
    monthly_gain: float
    last_weighed: str
    status: str


@dataclass
class RowRecord:
    '''
    This record stores common fields to both heifer and dam sheets and
    avoids using fields that are not common between the two
    '''
    tag: str
    farmer_name: str
    mbg: str
    code: str
    cow_no: str
    repaid: bool
    events: str
    breed: str
    semen: str
    born: str
    date_removed: str
    destination: str
    status: str
    is_dam: bool

    @classmethod
    def from_row(cls, row: pd.Series):
        '''
        Constructs this class using the provided row series

        :param row
            The pandas series that contain entries matching this class constructor
        '''
        return cls(
            tag=row['tag'].strip(),
            farmer_name=row['farmer_name'].strip(),
            mbg=row['mbg'].strip(),
            code=row['code'],
            cow_no=row['cow_no'],
            repaid=row['repaid'],
            events=row['events'],
            breed=row['breed'],
            semen=row['semen'],
            born=row['born'],
            date_removed=row['date_removed'],
            destination=row['destination'],
            status=row['status'],
            is_dam=row['is_dam']
        )

    def removal_records(self, df: pd.DataFrame) -> pd.DataFrame:
        '''
        With the given dataframe scan for rows that may contain transfer, death or
        sold data for the cow matching the tag of this record, if no record is
        found an empty data frame will be returned
        '''
        df_removal = pd.DataFrame({})

        return df_removal

    def to_dict(self) -> Dict[str, Any]:
        '''
        Returns the dictionary representation of the RowRecord type
        '''
        return {
            'tag': self.tag,
            'farmer_name': self.farmer_name,
            'mbg': self.mbg,
            'code': self.code,
            'cow_no': self.cow_no,
            'repaid': self.repaid,
            'events': self.events,
            'breed': self.breed,
            'semen': self.semen,
            'born': self.born,
            'date_removed': self.date_removed,
            'destination': self.destination,
            'status': self.status,
            'is_dam': self.is_dam,
        }


@dataclass
class DBRecord:
    '''
    Record to represent a typical entry in animal list from web
    '''
    tag: str
    herd: str
