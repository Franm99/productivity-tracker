import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# TODO separate matplotlib formatting from plotting


class Report:
    def __init__(self, records: dict[datetime.date], activity_set: list[str]):
        self.records = records
        self.daily_records = dict()
        self.activity_set = activity_set

    def daily_hours_per_activity(self, date: datetime.date) -> dict[int, int]:
        daily_records = self.records.get(date, None)

    def plot_time_per_activity(self, ax: plt.axis):
        seconds_spent = sum(self.total_secs_per_activity.values())

        def autopct_format(pctg):
            value = datetime.timedelta(seconds=round(seconds_spent * pctg / 100))
            return f'{pctg:.2f}%\n({value})'

        x = self.total_secs_per_activity.values()
        # TODO remove casting to int once the database saves int instead of str
        labels = [self.activity_set[int(key)] for key in self.total_secs_per_activity.keys()]

        ax.pie(x, labels=labels, autopct=autopct_format, wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'})

    def plot_intervals_in_day(self, ax: plt.axis, date: datetime.date):
        daily_records = self.records.get(date, None)

        if daily_records:
            base_dt = datetime.datetime.combine(date, datetime.datetime.min.time())  # Convert date to datetime

            ax.set_xlim(np.datetime64(str(base_dt + datetime.timedelta(hours=7, minutes=0))),
                        np.datetime64(str(base_dt + datetime.timedelta(hours=22, minutes=0))))

            ax.set_yticks(np.arange(len(self.activity_set)), labels=self.activity_set)
            ax.set_ylim(-0.5, len(self.activity_set) -0.5)

            locator = mdates.AutoDateLocator(minticks=12, maxticks=24)
            formatter = mdates.ConciseDateFormatter(locator)
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)

            intervals = dict()
            for record in daily_records:
                # TODO remove casting to int once database saves int instead of str
                start = base_dt + datetime.timedelta(seconds=int(record[2]))
                end = start + datetime.timedelta(seconds=int(record[1]))

                if record[0] not in intervals:
                    intervals[record[0]] = [[start, end]]
                else:
                    intervals[record[0]].append([start, end])

            for label_idx in intervals:
                # TODO remove casting to int once database saves int instead of str
                y = [int(label_idx)] * 2
                for interval in intervals[label_idx]:
                    x = interval
                    self.plot_day(x, y, linewidth=25, solid_capstyle='butt', color='blue')

    def plot_intervals(self, ax: plt.axis):

        if not self.records.keys():
            return []
        else:
            base_dt = list(self.records.keys())[0]
            base_dt = datetime.datetime.combine(base_dt, datetime.datetime.min.time())

        ax.set_xlim((np.datetime64(str(base_dt + datetime.timedelta(hours=6))),
                     np.datetime64(str(base_dt + datetime.timedelta(hours=22)))))

        ax.set_yticks(np.array(list(range(len(self.activity_set)))), labels=self.activity_set)
        ax.set_ylim(-0.5, 2.5)

        locator = mdates.HourLocator(interval=1)
        formatter = mdates.DateFormatter('%H:%M')

        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)

        for daily_records in self.records.values():
            intervals = self.compute_intervals(daily_records, base_dt)

            for label in intervals:
                y = [int(label)] * 2
                for interval in intervals[label]:
                    self.plot_day(interval, y, ax=ax, linewidth=25, solid_capstyle='butt', color=(0.2, 0.2, 0.2, 0.2))

    def show(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={'width_ratios': [1, 3]})

        self.plot_time_per_activity(ax1)
        self.plot_intervals(ax2)

        plt.show()

    @staticmethod
    def plot_day(x, y, ax=None, where='post', **kwargs):
        assert where in ['post', 'pre']
        x = np.array(x)
        y = np.array(y)

        y_slice = y[:-1] if where == 'post' else y[1:]

        X = np.c_[x[:-1], x[1:], x[1:]]
        Y = np.c_[y_slice, y_slice, np.zeros_like(x[:-1]) * np.nan]

        if not ax:
            ax = plt.gca()

        return ax.plot(X.flatten(), Y.flatten(), **kwargs)

    @staticmethod
    def compute_intervals(records, base_dt):
        intervals_per_activity = dict()
        for record in records:
            start = base_dt + datetime.timedelta(seconds=int(record[2]))
            end = start + datetime.timedelta(seconds=int(record[1]))

            if record[0] not in intervals_per_activity:
                intervals_per_activity[record[0]] = [[start, end]]
            else:
                intervals_per_activity[record[0]].append([start, end])

        return intervals_per_activity

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
