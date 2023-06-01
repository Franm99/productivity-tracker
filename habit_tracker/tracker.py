from datetime import datetime
import pathlib
import time

from .database.csv.database import CSVDatabase
from .report import Report


class Tracker:
    """
    Tracks user daily habits and stores them to a database.
    """
    # TODO make constructor generic to other types of database
    def __init__(self, date: datetime.date, db: CSVDatabase):
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

        self.is_tracking = False

    @classmethod
    def create_csv_tracker(cls, date: datetime.date, logs_dir: pathlib.Path = None):
        """
        Class method. Provides an interface to create a Tracker instance using a database based on CSV files.
        :param date: Day to be tracked.
        :param logs_dir: [Optional] Place to save CSV files.
        :return: Tracker instance
        """
        csv_database = CSVDatabase(logs_dir=logs_dir)
        return cls(date=date, db=csv_database)

    def start(self, activity: str) -> None:
        """
        Start tracking a new activity.
        :param activity: Current activity being performed.
        :return: None
        """
        self.current_activity = activity
        self.start_time = datetime.now().strftime("%H:%M:%S")  # TODO change to timestamp for easier postprocessing.
        self.interval_start = time.time()
        self.is_tracking = True

    def stop(self) -> None:
        """
        Stop tracking current activity.
        :return: None
        """
        if self.is_tracking:
            self.interval = int(time.time() - self.interval_start)
            self.is_tracking = False
        else:
            self.interval = 0

    def add_record(self) -> bool:
        """
        Add record to database.
        :return: False if couldn't add the record, True elsewhere.
        """
        if self.is_tracking:
            return False
        else:
            record = [self.current_activity, self.interval, self.start_time]
            self._db.update_log(self._date, record)
            return True

    def generate_report(self, start_date: datetime.date, end_date: datetime.date = None) -> Report:
        records = self._db.read_interval(start_date, end_date)
        return Report(records)
