from dataclasses import dataclass
from typing import Dict


@dataclass
class CalvingRecord:
    tag: str
    date: str


@dataclass
class DamRecord:
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


@dataclass
class TransferRecord:
    destination: str
    mbg: str
    date: str


@dataclass
class HeiferSheet:
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
