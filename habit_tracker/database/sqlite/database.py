from abc import ABC, abstractmethod
import sqlite3
from sqlite3 import Connection, Cursor
import datetime
import pathlib

from typing import List

from habit_tracker import settings

"""
TODO:
- Add logger
- TABLE HANDLING:
    * CONTROL DATA TO INSERT (EXPECTED FORMAT AND TYPE): -
    * 
- CRUD methods:
    * CREATE RECORD: 
        - SINGLE RECORD: OK
        - MULTIPLE RECORDS: -
    * DELETE RECORD:
        - FROM A CERTAIN DATE: -
        - FROM A 
    * UPDATE RECORD: -
    * GET RECORD:
        - FROM ACTIVITY NAME: -
        - FROM DURATION: -
        - FROM A GIVEN TIME INTERVAL: -
        - HOW TO RETRIEVE:
            - FORMATTED (timestamp to date, duration to h:m:s): -
            - 
            
            
DATABASE
UI
DATA VISUALIZATION

- 
"""

# TODO: add logger to abstract class


class SqliteDatabase:
    def __init__(self, name: str):
        self._name = name
        self._conn: Connection = sqlite3.connect(settings.DB_DIR / 'sqlite3.db')
        self._cur: Cursor = self._conn.cursor()

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
        table = self._cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")\
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


if __name__ == '__main__':
    sqliteDb = SqliteDatabase("sample")
    sqliteDb.connect_with_table('sample', ['timestamp', 'activity', 'duration', 'description'])
    sqliteDb.add_record(int(datetime.datetime(2024, 5, 15, 11, 34, 22).timestamp()), "a1", 2000)
    sqliteDb.add_record(datetime.datetime(2024, 5, 15, 14, 30, 10).timestamp().__int__(), "a2", 2000, "desc1")
    sqliteDb.add_record(datetime.datetime(2024, 4, 25, 14, 30, 10).timestamp().__int__(), "a3", 2000, "desc3")
    sqliteDb.add_record(datetime.datetime(2024, 5, 5, 14, 30, 10).timestamp().__int__(), "a4", 2000, "awdada")
    sqliteDb.add_record(datetime.datetime(2024, 6, 24, 14, 30, 10).timestamp().__int__(), "a5", 2000, "75644")
    print(sqliteDb._cur.execute('SELECT * FROM sample').fetchall())



