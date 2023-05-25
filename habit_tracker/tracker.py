from datetime import datetime
import pathlib
import time

from typing import List

from .database import CSVDatabase
from .report import DailyReport, WeeklyReport, MonthlyReport
from .utils import DEF_LOGS_DIR, ReportType


params = ["activity", "interval", "start_time"]


class Tracker:
    """
    Tracks user habits and saves them to the database.
    """
    def __init__(self, date: str, logs_dir: pathlib.Path = DEF_LOGS_DIR):
        self._date = date
        self._logs_dir = logs_dir
        self._log_file = logs_dir / f"{self._date}.csv"

        self.db = CSVDatabase(self._log_file, fieldnames=params)

        self.current_activity: str = ''
        self.start_timestamp = 0.0
        self.start_hour = None
        self.interval = 0

    def start(self, activity):
        """
        Start tracking a new user activity.
        :return:
        """
        self.current_activity = activity
        self.start_hour = datetime.now().strftime("%H:%M:%S")
        self.start_timestamp = time.time()

    def stop(self):
        """
        Stop tracking activity.
        :return: Time spent in last activity.
        """
        # TODO: add logic to catch if stop is called before start.
        self.interval = int(time.time() - self.start_timestamp)

    def add_track(self):
        record = {
            params[0]: self.current_activity,
            params[1]: self.interval,
            params[2]: self.start_hour
        }
        self.db.update(**record)

    def generate_report(self, type_: ReportType):
        """
        Generates a Report class based on the tracked data.
        """
        if type_ == ReportType.DAY:
            return DailyReport(self.db)
        elif type_ == ReportType.WEEK:
            raise NotImplementedError("Weekly report not supported yet.")
        elif type_ == ReportType.MONTH:
            raise NotImplementedError("Monthly report not supporetd yet.")

