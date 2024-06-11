import logging
import sqlite3
from sqlite3 import Connection, Cursor

logger = logging.getLogger(__name__)


class HabitsTable:

    def __init__(self, name: str, conn: Connection):
        self._name = name
        self._conn = conn
        self._cursor = self._conn.cursor()
        self._columns = [
            "timestamp",
            "activity",
            "duration",
            "description"
        ]

    def exists_in_db(self):
        table = self._cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self._name}'") \
            .fetchone()
        return True if table else False

    def create(self, name: str, overwrite: bool = False):
        if self.exists_in_db():
            logger.warning(f"Table {self._name} has already been defined in the current database.")
            if not overwrite:
                logger.info(f"Selecting existing table. Use overwrite=True to overwrite.")
            else:
                logger.warning(f"Overwriting existing table.")
                self._cursor.execute(f"DROP TABLE '{self._name}'")
                self._cursor.execute(f"CREATE TABLE {self._name}({', '.join(self._columns)}")
                self._conn.commit()
        else:
            logger.info(f"Creating new table with name '{self._name}'")
            self._cursor.execute(f"CREATE TABLE {self._name}({', '.join(self._columns)}")
            self._conn.commit()

    def select_all(self):
        return []

    def __len__(self):
        return len(self.select_all())

    @property
    def name(self) -> str:
        return self._name

    @property
    def columns(self) -> list[str]:
        return self._columns


