from datetime import datetime
import pathlib
import time

from .database import RDBMS, CSVDatabase
from .report import Report, DailyReport  # , WeeklyReport, MonthlyReport
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
        self.start_time = None
        self.interval_start = None
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

    def start(self, activity: str) -> None:
        """
        Start tracking a new activity.
        :param activity: Current activity being performed.
        :return: None
        """
        self.current_activity = activity
        self.start_time = datetime.now().strftime("%H:%M:%S")
        self.interval_start = time.time()

    def stop(self) -> None:
        """
        Stop tracking current activity.
        :return: None
        """
        # TODO: add logic to catch if stop is called before start.
        self.interval = int(time.time() - self.interval_start)

    def add_record(self) -> None:
        """
        Add record to database.
        :return: None
        """
        record = {
            CSV_FIELDNAMES[0]: self.current_activity,
            CSV_FIELDNAMES[1]: self.interval,
            CSV_FIELDNAMES[2]: self.start_time
        }
        self._db.update(**record)

    def generate_report(self, type_: ReportType) -> Report:
        """
        Generates a report (Daily, Weekly or Monthly) about records in the database for the user.
        :param type_: Type of report to be retrieved.
        :return: Report
        """
        if type_ == ReportType.DAY:
            return DailyReport(self._db)
        elif type_ == ReportType.WEEK:
            raise NotImplementedError("Weekly report not supported yet.")
        elif type_ == ReportType.MONTH:
            raise NotImplementedError("Monthly report not supported yet.")

