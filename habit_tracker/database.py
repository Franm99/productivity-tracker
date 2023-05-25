import csv
import pathlib

from abc import ABC, abstractmethod
from typing import List


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
    def update(self, **kwargs):
        pass

    @abstractmethod
    def delete(self):
        pass


class CSVDatabase(RDBMS):
    def __init__(self, file_path: pathlib.Path, fieldnames: List[str]):
        super().__init__()

        self._file_path = file_path
        self._logs_dir = file_path.parent

        self._fieldnames = fieldnames
        self.create()

    def create(self):
        if not self._logs_dir.exists():
            self._logs_dir.mkdir(parents=True)

        if not self._file_path.exists():
            with open(self._file_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self._fieldnames)
                writer.writeheader()

    def read(self):
        try:
            with open(self._file_path, "r") as f:
                csv_reader = csv.reader(f, delimiter=",")
                return [row for row in csv_reader][1:]
        except FileNotFoundError:
            return []

    def update(self, **kwargs):
        with open(self._file_path, "a+", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self._fieldnames)
            writer.writerow(kwargs)

    def delete(self):
        self._file_path.unlink()

    @property
    def file_path(self):
        return self._file_path
