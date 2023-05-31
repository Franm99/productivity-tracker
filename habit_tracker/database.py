import csv
import datetime
import pathlib
import warnings

from math import ceil
from typing import Optional

from .utils import DEF_LOGS_DIR, CSV_FIELDNAMES


class CSVLog:
    def __init__(self, date: datetime.date, logs_dir: pathlib.Path = None):
        self._date = date
        self._year = str(date.year)
        self._month = str(date.month).zfill(2)
        self._week = str(self._week_of_month()).zfill(2)
        self._day_of_week = str(self._date.weekday()).zfill(2)
        self._day = str(date.day).zfill(2)

        self._fieldnames = CSV_FIELDNAMES

        self._logs_dir = logs_dir if logs_dir else DEF_LOGS_DIR
        self._file = self._logs_dir / self._year / self._month / self._week / f"{self._day_of_week}.csv"

    @classmethod
    def new(cls, date: datetime.date, logs_dir: pathlib.Path = None):
        csv_log = cls(date, logs_dir)
        csv_log.create()  # If log was already created, this won't do anything.
        return csv_log

    def create(self):
        if not self._file.parent.exists():
            self._file.parent.mkdir(parents=True)
        if not self.exists():
            open(self._file, mode="a").close()

    def exists(self):
        return self._file.exists()

    def read(self) -> Optional[list[list[str]]]:
        if self.exists() and self._file.stat().st_size > 0:
            with open(self._file, "r") as f:
                csv_reader = csv.reader(f, delimiter=",")
                return [row for row in csv_reader]  # TODO think about how to use generator here
        else:
            return []

    def update(self, activity: str, interval: str, start_time: str):
        if not self.exists():
            self.create()

        with open(self._file, "a+", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([activity, interval, start_time])

    def delete(self):
        if self.exists():
            self._file.unlink()

    def _week_of_month(self):
        first_day = self._date.replace(day=1)
        dom = self._date.day
        adjusted_dom = dom + first_day.weekday()
        return int(ceil(adjusted_dom / 7.0))

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def week(self):
        return self._week

    @property
    def day(self):
        return self._day

    @property
    def day_of_week(self):
        return self._day_of_week


class CSVDatabase:
    """ Interface to operate with a CSV file as a database."""
    # def __init__(self, file_path: pathlib.Path, fieldnames: List[str]):
    def __init__(self, logs_dir: pathlib.Path = None):
        self._logs_dir = logs_dir if logs_dir else DEF_LOGS_DIR

    def read_log(self, date: datetime.date) -> list[list[str]]:
        """
        Read the full content of the current CSV file.
        :return: List of rows of the CSV file.
        """
        return CSVLog(date, logs_dir=self._logs_dir).read()

    def update_log(self, date: datetime.date, values: list[str]):
        CSVLog(date, self._logs_dir).update(*values)

    def delete_log(self, date: datetime.date) -> None:
        CSVLog(date, logs_dir=self._logs_dir).delete()

    def read_interval(self, start_date: datetime.date, end_date: datetime.date = None) -> Optional[dict]:
        if (end_date is None) or (start_date == end_date):
            return {start_date: CSVLog(start_date, self._logs_dir).read()}
        else:
            interval_records = dict()
            if end_date < start_date:
                warnings.warn("Not valid interval: end date is earlier than the start date.", category=UserWarning)
                return interval_records
            days = (end_date - start_date).days
            for t_delta in range(days + 1):
                date = start_date + datetime.timedelta(days=t_delta)
                interval_records[date] = CSVLog(date, self._logs_dir).read()
            return interval_records
