from enum import Enum, auto
from pathlib import Path

DEF_LOGS_DIR = Path('daily_logs')

CSV_FIELDNAMES = ["activity", "interval", "start_time"]


class ReportType(Enum):
    DAY = auto()
    WEEK = auto()
    MONTH = auto()


class Activity(Enum):
    PROJECTS = 0
    HOUSE = 1
    REST = 2
    STUDY = 3
    SPORT = 4
    LEISURE = 5
