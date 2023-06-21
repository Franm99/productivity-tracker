import datetime

from .plots import Graphics


class Report:
    def __init__(self, records: dict[datetime.date], activity_set: list[str]):
        self.records = records
        self.daily_records = dict()
        self.activity_set = activity_set
        self.graphics = Graphics()

    def plot_time_per_activity(self):

        x = self.total_secs_per_activity.values()
        labels = [self.activity_set[int(key)] for key in self.total_secs_per_activity.keys()]

        def auto_pct(pct):
            total_secs = round(sum(self.total_secs_per_activity.values()))
            return f'{pct:.2f}%\n({datetime.timedelta(seconds=total_secs)}'

        self.graphics.pie(x, labels, auto_pct, {'linewidth': 3.0, 'edgecolor': 'white'})

    def plot_intervals(self):
        self.graphics.workday(self.records, self.activity_set)

    def show(self):
        self.plot_time_per_activity()
        self.plot_intervals()
        self.graphics.show()

    @property
    def total_secs_per_activity(self) -> dict[int, int]:
        """
        Returns the total amount of seconds spent in a specific activity along the set of days that are registered
        in the report.
        """
        time_per_activity = dict()
        for daily_records in self.records.values():
            for entry in daily_records:
                time_per_activity[entry[0]] = time_per_activity.get(entry[0], 0) + int(entry[1])
        return time_per_activity
