import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from datetime import date, timedelta

from .database import CSVDatabase
from .utils import DEF_LOGS_DIR


class DailyReport:
    def __init__(self, db: CSVDatabase):
        self._db = db
        self._date = db.file_path.stem
        self.records = dict()

    def compute_totals(self):
        tracks = self._db.read()
        for track in tracks:
            self.records[track[0]] = int(track[1]) + self.records.get(track[0], 0)

    def show(self):
        plt.figure()
        seconds_spent = sum(self.records.values())

        def autopct_format(pctg):
            value = timedelta(seconds=round(seconds_spent * pctg / 100))
            return f'{pctg:.2f}%\n({value})'

        plt.pie(self.records.values(), labels=self.records.keys(), autopct=autopct_format,
                wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'})
        plt.title(self._date)
        plt.tight_layout()
        plt.show()


class WeeklyReport:
    def __init__(self):
        pass


class MonthlyReport:
    def __init__(self):
        pass
