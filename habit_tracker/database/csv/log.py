import csv
import datetime
import pathlib

from math import ceil
from typing import Optional

class CSVLog:
    def __init__(self, date: datetime.date, base_dir: pathlib.Path):
        self._date = date
        self._year = str(date.year)
        self._month = str(date.month).zfill(2)
        self._week = str(self._week_of_month()).zfill(2)
        self._day_of_week = str(self._date.weekday()).zfill(2)
        self._day = str(date.day).zfill(2)

        self._base_dir = base_dir
        self._file = self._base_dir / self._year / self._month / self._week / f"{self._day_of_week}.csv"

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
                # TODO: save integer values as integers instead of strings
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
    def date(self):
        return self._date
