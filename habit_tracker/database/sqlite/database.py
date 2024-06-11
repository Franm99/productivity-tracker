import sqlite3
from sqlite3 import Connection, Cursor
import datetime
import logging

from typing import List

from habit_tracker import settings
from habit_tracker.database.sqlite.HabitsTable import HabitsTable

logger = logging.getLogger(__name__)


class DBModel:

    def __init__(self, db_name: str):
        self._name = db_name
        self._conn: Connection = sqlite3.connect(settings.DB_DIR / 'sqlite3.db')
        self._cur: Cursor = self._conn.cursor()
        self._db_name: str
        self._db_type: str  # Sqlite, PostgresQL, MySQL, CSV, etc.
        self._active_table: HabitsTable
        self._table_set: list[HabitsTable]
        self._conn: Connection
        self._cur: Cursor

    def connect_with_table(self, table_name: str, headers: List[str]):
        """
        Creates a new sqlite3 table with the given headers.

        :param table_name:
        :param headers:
        :return:
        """
        if not self.table_exists(table_name):
            self._cur.execute(f"CREATE TABLE {self._name}({', '.join(headers)})")

    def table_exists(self, table_name: str):
        table = self._cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'") \
            .fetchone()
        return True if table else False

    def add_record(self, timestamp: int, name: str, duration: int, desc: str = None):
        """

        :param timestamp:
        :param name:
        :param duration:
        :param desc:
        :return:
        """
        self._cur.execute(
            f"""
            INSERT INTO {self._name} VALUES(
            {timestamp},
            '{name}',
            {duration},
            '{desc if desc else ""}')
            """
        )
        self._conn.commit()

    def create_table(self, name):
        pass

    def is_table_present(self, name):
        pass

    def drop_table(self, name):
        pass

    def add_records(self, records: List):
        pass

    def drop_last_record(self):
        pass

    def drop_record_from_date(self, date: datetime):
        pass

    def get_all_records(self):
        pass

    def get_records_from_activity(self, activity: str = None):
        pass

    def get_records_for_period(self, start_date: datetime = None, end_date: datetime = None):
        pass

    def get_longest_activities(self, min_duration: datetime.time):
        pass

    """GETTERS/SETTERS"""
    def get_activities_from_table(self, table_name: str) -> list:
        pass


# if __name__ == '__main__':
#     sqliteDb = DBModel("sample")
#     sqliteDb.connect_with_table('sample', ['timestamp', 'activity', 'duration', 'description'])
#     sqliteDb.add_record(int(datetime.datetime(2024, 5, 15, 11, 34, 22).timestamp()), "a1", 2000)
#     sqliteDb.add_record(datetime.datetime(2024, 5, 15, 14, 30, 10).timestamp().__int__(), "a2", 2000, "desc1")
#     sqliteDb.add_record(datetime.datetime(2024, 4, 25, 14, 30, 10).timestamp().__int__(), "a3", 2000, "desc3")
#     sqliteDb.add_record(datetime.datetime(2024, 5, 5, 14, 30, 10).timestamp().__int__(), "a4", 2000, "awdada")
#     sqliteDb.add_record(datetime.datetime(2024, 6, 24, 14, 30, 10).timestamp().__int__(), "a5", 2000, "75644")
#     print(sqliteDb._cur.execute('SELECT * FROM sample').fetchall())



