import datetime
import pathlib
import warnings
import json

from pydantic import BaseModel
from typing import Optional

from .log import CSVLog

DEF_BASE_DIR = pathlib.Path('.db')


class DBMetadata(BaseModel):
    name: str
    activities: list[str]
    par_dir: pathlib.Path

    @property
    def dir_path(self):
        return self.par_dir / pathlib.Path(self.name)

    @property
    def file(self):
        return self.dir_path / pathlib.Path("metadata.json")


class CSVDatabase:
    """ Interface to operate with a CSV file as a database."""
    def __init__(self, metadata: DBMetadata):
        self.metadata = metadata

        if not self.metadata.dir_path.is_dir():
            self.metadata.dir_path.mkdir(parents=True)
            with open(self.metadata.file, "w") as f:
                json_string = self.metadata.json(indent=4)
                f.write(json_string)

    @classmethod
    def create(cls, name: str, activities: list[str], par_dir: pathlib.Path):
        metadata = DBMetadata(name=name, activities=activities, par_dir=par_dir)
        metadata.dir_path.mkdir(parents=True)
        with open(metadata.file, "w") as f:
            json_string = metadata.json(indent=4)
            f.write(json_string)
        return cls(metadata)

    @classmethod
    def load_from_metadata(cls, name: str, par_dir: pathlib.Path):
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
        return CSVLog(date, base_dir=self.metadata.dir_path).read()

    def update_log(self, date: datetime.date, values: list[str]):
        # TODO check that the activity is in the activity set
        CSVLog(date, self.metadata.dir_path).update(*values)

    def delete_log(self, date: datetime.date) -> None:
        CSVLog(date, base_dir=self.metadata.dir_path).delete()

    def read_interval(self, start_date: datetime.date, end_date: datetime.date = None) -> Optional[dict]:
        if (end_date is None) or (start_date == end_date):
            return {start_date: CSVLog(start_date, self.metadata.dir_path).read()}
        else:
            interval_records = dict()
            if end_date < start_date:
                warnings.warn("Not valid interval_seconds: end date is earlier than the start date.",
                              category=UserWarning)
                return interval_records
            days = (end_date - start_date).days
            for t_delta in range(days + 1):
                date = start_date + datetime.timedelta(days=t_delta)
                interval_records[date] = CSVLog(date, self.metadata.dir_path).read()
            return interval_records
