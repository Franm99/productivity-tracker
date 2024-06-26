# TODO consider using pandas: intervals can be computed in-site or in a new df.

import datetime
import pathlib
import warnings
import json

from typing import Optional

# TODO: check imports as modules
from .log import CSVLog
from .metadata import DBMetadata

DEF_BASE_DIR = pathlib.Path('.db')

# TODO reformat database tree folder: use year/month/days instead of year/month/week/weekday.


class CSVDatabase:
    """ Interface to operate with a CSV file as a database."""

    # TODO: track set of existing databases to check if a db already exists.

    def __init__(self, metadata: DBMetadata):
        self.metadata = metadata

    @classmethod
    def create(cls, name: str, activities: list[str], par_dir: pathlib.Path):
        metadata = DBMetadata(name=name, activities=activities, par_dir=par_dir)
        metadata.db_path.mkdir(parents=True)
        with open(metadata.file, "w") as f:
            json_string = metadata.model_dump_json(indent=4)
            f.write(json_string)
        return cls(metadata)

    @classmethod
    def load_from_name(cls, name: str, par_dir: pathlib.Path):
        metadata_file = par_dir / pathlib.Path(name) / pathlib.Path("metadata.json")
        try:
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
                return cls(DBMetadata(**metadata))
        except FileNotFoundError:
            return None

    def read_log(self, date: datetime.date) -> list[list[str]]:
        """
        Read the full content of the current CSV file.
        :return: List of rows of the CSV file.
        """
        return CSVLog(date, base_dir=self.metadata.db_path).read()

    def update_log(self, date: datetime.date, values: list[str]):
        # TODO check that the activity is in the activity set
        CSVLog(date, self.metadata.db_path).update(*values)

    def delete_log(self, date: datetime.date) -> None:
        CSVLog(date, base_dir=self.metadata.db_path).delete()

    def read_interval(self, start_date: datetime.date, end_date: datetime.date = None) -> Optional[dict]:
        if (end_date is None) or (start_date == end_date):
            return {start_date: CSVLog(start_date, self.metadata.db_path).read()}
        else:
            interval_records = dict()
            if end_date < start_date:
                warnings.warn("Not valid interval_seconds: end date is earlier than the start date.",
                              category=UserWarning)
                return interval_records
            days = (end_date - start_date).days
            for t_delta in range(days + 1):
                date = start_date + datetime.timedelta(days=t_delta)
                interval_records[date] = CSVLog(date, self.metadata.db_path).read()
            return interval_records

    @property
    def name(self):
        return self.metadata.name

    def __eq__(self, other):
        return self.metadata.file == other.metadata.file
