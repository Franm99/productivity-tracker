import logging
import sqlite3
from sqlite3 import Connection
from habit_tracker import settings
from typing import Optional
from enum import Enum

logger = logging.getLogger(__name__)

HABITS_TABLE_COLS = (
    'timestamp',
    'name',
    'duration'
)


def connect_to_db() -> Optional[Connection]:

    if not settings.DB_DIR.exists():
        settings.DB_DIR.mkdir(parents=True)

    try:
        conn = sqlite3.connect(settings.DB_DIR / '.db')
        logger.info("Successfully connected to database.")
        return conn
    except sqlite3.Error:
        logger.error("Cannot connect to database.")
        return None


def create_table(conn: Connection, name: str, cols: list[tuple]) -> int:
    """

    :param conn:
    :param name:
    :param cols:
    :return: 0: OK; 1: ALREADY CREATED; 2: ERROR
    """
    cur = conn.cursor()
    cols_and_types = ', '.join([f"{n} {t}" for (n, t) in cols])
    result = 0
    try:
        cur.execute(f"CREATE TABLE {name}({cols_and_types})")
        conn.commit()
    except sqlite3.OperationalError:
        logger.warning(f"Table with name '{name}' already exists.")
        result = 1
    except sqlite3.Error:
        logger.error("An error occurred while trying to create a table.")
        result = 2
    finally:
        cur.close()
        return result


def create_habits_table(conn: Connection, name: str) -> int:
    """

    :param conn:
    :param name:
    :return: 0: OK; 1: ALREADY CREATED; 2: ERROR
    """
    HABITS_TABLE_COLS_AND_TYPES = [
        ("timestamp", "INTEGER PRIMARY KEY"),
        ("name", "text NOT NULL"),
        ("duration", "INTEGER NOT NULL")
    ]

    return create_table(conn, name, HABITS_TABLE_COLS_AND_TYPES)


def insert_record(conn: Connection, table_name: str, record: tuple) -> bool:
    if len(record) != len(HABITS_TABLE_COLS):
        logger.error(f"Insert query not permitted. Should contain {len(HABITS_TABLE_COLS)} values.")
        return False

    cur = conn.cursor()
    result = True

    try:
        query = f"""
        INSERT INTO {table_name}
        ({', '.join(HABITS_TABLE_COLS)})
        VALUES
        (?, ?, ?) 
        """
        cur.execute(query, record)
        conn.commit()
        logger.info(f"Successfully added record to table {table_name}")
    except sqlite3.Error as e:
        logger.error(f'Could not perform INSERT query. Error trace: {e}')
        result = False
    finally:
        logger.info("Closing connection to database.")
        cur.close()
        return result


def select_all(conn: Connection, table_name: str):
    cur = conn.cursor()
    records = None
    try:
        query = f"""SELECT * FROM {table_name}"""
        cur.execute(query)
        records = cur.fetchall()
    except sqlite3.Error as e:
        logger.error(f"Could not perform SELECT query. Error trace: {e}")
    finally:
        logger.info('Closing connection to database.')
        cur.close()
        return records


def select_action(conn: Connection, table_name: str, action_name: str):
    cur = conn.cursor()
    records = None
    try:
        query = f"""SELECT * FROM {table_name} WHERE name = '{action_name}'"""
        cur.execute(query)
        records = cur.fetchall()
    except sqlite3.Error as e:
        logger.error(f"Could not perform SELECT query. Error trace: {e}")
    finally:
        logger.info('Closing connection to database.')
        cur.close()
        return records


def select_actions_with_min_duration(conn: Connection, table_name: str, min_duration: int):
    cur = conn.cursor()
    records = None
    try:
        query = f"""SELECT * FROM {table_name} WHERE duration > {min_duration}"""
        cur.execute(query)
        records = cur.fetchall()
    except sqlite3.Error as e:
        logger.error(f"Could not perform SELECT query. Error trace: {e}")
    finally:
        logger.info('Closing connection to database.')
        cur.close()
        return records


def main(table_name: str):
    import datetime

    conn = connect_to_db()
    # create_table(conn, table_name, [
    #     ("timestamp", "INTEGER PRIMARY KEY"),
    #     ("name", "text NOT NULL"),
    #     ("duration", "INTEGER NOT NULL")
    # ])
    #
    # insert_record(conn, table_name, (datetime.datetime(2024, 3, 10, 6, 30).timestamp(), "workout", 1800))
    # insert_record(conn, table_name, (datetime.datetime(2024, 3, 10, 7).timestamp(), "shower", 600))
    # insert_record(conn, table_name, (datetime.datetime(2024, 3, 10, 7, 10).timestamp(), "breakfast", 900))
    # insert_record(conn, table_name, (datetime.datetime(2024, 3, 10, 7, 25).timestamp(), "study", 1800))
    # insert_record(conn, table_name, (datetime.datetime(2024, 3, 10, 7, 55).timestamp(), "rest", 300))
    # insert_record(conn, table_name, (datetime.datetime(2024, 3, 10, 8, 0).timestamp(), "work", 14400))
    # insert_record(conn, table_name, (datetime.datetime(2024, 3, 10, 12, 0).timestamp(), "rest", 1800))
    # insert_record(conn, table_name, (datetime.datetime(2024, 3, 10, 12, 30).timestamp(), "work", 14400))
    #
    # records = select_all(conn, table_name)
    # print(records)
    #
    # records = select_action(conn, table_name, 'rest')
    # print(records)
    # records = select_action(conn, table_name, 'work')
    # print(records)
    #
    # records = select_actions_with_min_duration(conn, table_name, 1500)
    # print(records)
    # records = select_actions_with_min_duration(conn, table_name, 14000)
    # print(records)


if __name__ == '__main__':
    import sys

    logFormatter = logging.Formatter("[%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger(__name__)

    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    main('habits')
