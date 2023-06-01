import datetime
import pathlib
import warnings

from typing import Optional

from .log import CSVLog

DEF_BASE_DIR = pathlib.Path('daily_logs')


class CSVDatabase:
    """ Interface to operate with a CSV file as a database."""
    # def __init__(self, file_path: pathlib.Path, fieldnames: List[str]):
    def __init__(self, logs_dir: pathlib.Path = None):
        self._logs_dir = logs_dir if logs_dir else DEF_BASE_DIR

    def read_log(self, date: datetime.date) -> list[list[str]]:
        """
        Read the full content of the current CSV file.
        :return: List of rows of the CSV file.
        """
        return CSVLog(date, base_dir=self._logs_dir).read()

    def update_log(self, date: datetime.date, values: list[str]):
        CSVLog(date, self._logs_dir).update(*values)

    def delete_log(self, date: datetime.date) -> None:
        CSVLog(date, base_dir=self._logs_dir).delete()

    def read_interval(self, start_date: datetime.date, end_date: datetime.date = None) -> Optional[dict]:
        if (end_date is None) or (start_date == end_date):
            return {start_date: CSVLog(start_date, self._logs_dir).read()}
        else:
            interval_records = dict()
            if end_date < start_date:
                warnings.warn("Not valid interval_seconds: end date is earlier than the start date.",
                              category=UserWarning)
                return interval_records
            days = (end_date - start_date).days
            for t_delta in range(days + 1):
                date = start_date + datetime.timedelta(days=t_delta)
                interval_records[date] = CSVLog(date, self._logs_dir).read()
            return interval_records
