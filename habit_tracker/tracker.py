from datetime import datetime
import pathlib
import time

from .database import RDBMS, CSVDatabase
from .report import DailyReport  # , WeeklyReport, MonthlyReport
from .utils import CSV_FIELDNAMES, DEF_LOGS_DIR, ReportType


class Tracker:
    """
    Tracks user daily habits and stores them to a database.
    """
    def __init__(self, date: str, db: RDBMS):
        """
        Class Constructor.
        :param date: Day to be tracked.
        :param db: Database to use.
        """
        self._date = date
        self._db = db

        self.current_activity: str = ''
        self.start_timestamp = 0.0
        self.start_hour = None
        self.interval = 0

    @classmethod
    def create_csv_tracker(cls, date: str, logs_dir: pathlib.Path = DEF_LOGS_DIR):
        """
        Class method. Provides an interface to create a Tracker instance using a database based on CSV files.
        :param date: Day to be tracked.
        :param logs_dir: [Optional] Place to save CSV files.
        :return: Tracker instance
        """
        log_file = logs_dir / f"{date}.csv"
        csv_database = CSVDatabase(log_file, fieldnames=CSV_FIELDNAMES)
        return cls(date=date, db=csv_database)

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
            CSV_FIELDNAMES[0]: self.current_activity,
            CSV_FIELDNAMES[1]: self.interval,
            CSV_FIELDNAMES[2]: self.start_hour
        }
        self._db.update(**record)

    def generate_report(self, type_: ReportType):
        """
        Generates a Report class based on the tracked data.
        """
        if type_ == ReportType.DAY:
            return DailyReport(self._db)
        elif type_ == ReportType.WEEK:
            raise NotImplementedError("Weekly report not supported yet.")
        elif type_ == ReportType.MONTH:
            raise NotImplementedError("Monthly report not supporetd yet.")

