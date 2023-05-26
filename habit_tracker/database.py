import csv
import pathlib

from abc import ABC, abstractmethod
from typing import List

# TODO refactor how database saves data: create weeks and months folders

class RDBMS(ABC):
    """
    Generic Relational DataBase Management System.
    """
    def __init__(self):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def update(self, **kwargs) -> bool:
        pass

    @abstractmethod
    def delete(self):
        pass


class CSVDatabase(RDBMS):
    """ Interface to operate with a CSV file as a database."""
    def __init__(self, file_path: pathlib.Path, fieldnames: List[str]):
        """
        Class constructor.
        :param file_path: Full path to CSV file.
        :param fieldnames: column names for CSV file.
        """
        super().__init__()

        self._file_path = file_path
        self._logs_dir = file_path.parent

        self._fieldnames = fieldnames
        self.create()

    def create(self) -> None:
        """
        Creates a new CSV file to be used as database.
        :return:
        """
        if not self._logs_dir.exists():
            self._logs_dir.mkdir(parents=True)

        if not self._file_path.exists():
            with open(self._file_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self._fieldnames)
                writer.writeheader()

    def read(self) -> List[List[str]]:
        """
        Read the full content of the current CSV file.
        :return: List of rows of the CSV file.
        """
        try:
            with open(self._file_path, "r") as f:
                csv_reader = csv.reader(f, delimiter=",")
                return [row for row in csv_reader][1:]
        except FileNotFoundError:
            return []

    def update(self, **kwargs) -> bool:
        """
        Creates a new entry (new row) on the CSV file.
        :param kwargs: Key-value pairs to add to the row.
        :return: None
        """
        try:
            with open(self._file_path, "a+", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self._fieldnames)
                writer.writerow(kwargs)
            return True
        except OSError:
            return False

    def delete(self) -> None:
        """
        Deletes the current CSV file.
        :return:
        """
        self._file_path.unlink()

    @property
    def file_path(self):
        """ Full path to the CSV file. """
        return self._file_path


class MySQLDatabase(RDBMS):
    def __init__(self):
        super().__init__()

    def create(self):
        pass

    def read(self):
        pass

    def update(self, **kwargs):
        pass

    def delete(self):
        pass

