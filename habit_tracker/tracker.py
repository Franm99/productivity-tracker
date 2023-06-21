import datetime
import time

from dataclasses import dataclass, asdict
from typing import Optional

from .database.csv.database import CSVDatabase
from .report import Report


@dataclass
class Record:
    activity: int
    interval_seconds: int
    seconds_from_start: int

    def values(self) -> list:
        return [str(val) for val in asdict(self).values()]


class Tracker:
    """
    Tracks user daily habits and stores them to a database.
    """
    # TODO make constructor generic to other types of database
    def __init__(self, db: CSVDatabase, date: datetime.date = datetime.date.today()):
        self._db = db
        self._date = date

        self._current_activity_idx: int = -1
        self._seconds_from_base_date: int = 0
        self._interval_start: int = 0
        self._interval_seconds: int = 0
        self._record: Optional[Record] = None
        self._is_tracking: bool = False

    def start(self, activity_idx: int) -> None:
        self._current_activity_idx = activity_idx

        now = datetime.datetime.now()
        timedelta = datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
        self._seconds_from_base_date = int(timedelta.total_seconds())

        self._interval_start = time.time()
        self._is_tracking = True

    def stop(self) -> None:
        """
        Stop tracking current activity.
        :return: None
        """
        if self._is_tracking:
            self._interval_seconds = int(time.time() - self._interval_start)
            self._is_tracking = False
        else:
            self._interval_seconds = 0

        record = Record(self._current_activity_idx, self._interval_seconds, self._seconds_from_base_date)
        self.add_record(record)

    def add_record(self, record: Record) -> bool:
        """
        Add record to database.
        :return: False if couldn't add the record, True elsewhere.
        """
        if self._is_tracking:
            return False
        else:
            self._db.update_log(self._date, record.values())
            return True

    def generate_report(self, start_date: str, end_date: str = None) -> Report:
        if start_date == 'today':
            records = self._db.read_interval(self._date)

        else:
            start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y")
            end_date = datetime.datetime.strptime(end_date, "%d-%m-%Y") if end_date else None
            records = self._db.read_interval(start_date, end_date)

        return Report(records, activity_set=self._db.metadata.activities)

    @property
    def activity_set(self):
        return self._db.metadata.activities
