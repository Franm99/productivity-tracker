import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# TODO separate matplotlib formatting from plotting


class Report:

    plt.style.use('seaborn-v0_8-darkgrid')

    def __init__(self, records: dict[datetime.date], activity_set: list[str]):
        self.records = records
        self.daily_records = dict()
        self.activity_set = activity_set

    def daily_hours_per_activity(self, date: datetime.date) -> dict[int, int]:
        daily_records = self.records.get(date, None)

        total_per_activity = dict()
        if daily_records:
            for record in daily_records:
                # accumulate seconds from different records on each activity
                total_per_activity[record[0]] = int(record[1]) + total_per_activity.get(record[0], 0)

        return total_per_activity

    def show_daily_report(self, date: datetime.date = None):
        date = date if date else datetime.date.today()
        self.plot_time_per_activity(date)
        self.plot_intervals_in_day(date)
        plt.show()

    def plot_time_per_activity(self, date: datetime.date) -> tuple[plt.Figure, plt.Axes]:
        total_per_activity = self.daily_hours_per_activity(date)

        fig, ax = plt.subplots(1, 1)
        seconds_spent = sum(total_per_activity.values())

        def autopct_format(pctg):
            value = datetime.timedelta(seconds=round(seconds_spent * pctg / 100))
            return f'{pctg:.2f}%\n({value})'

        x = total_per_activity.values()
        # TODO remove casting to int once the database saves int instead of str
        labels = [self.activity_set[int(key)] for key in total_per_activity.keys()]

        ax.pie(x, labels=labels, autopct=autopct_format, wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'})
        ax.set_title(date)
        fig.tight_layout()

        return fig, ax

    def plot_intervals_in_day(self, date: datetime.date) -> tuple[plt.Figure, plt.Axes]:
        daily_records = self.records.get(date, None)

        if daily_records:
            base_dt = datetime.datetime.combine(date, datetime.datetime.min.time())  # Convert date to datetime

            fig, ax = plt.subplots(1, 1, figsize=(14, 5))
            ax.set_xlim(np.datetime64(str(base_dt + datetime.timedelta(hours=7, minutes=0))),
                        np.datetime64(str(base_dt + datetime.timedelta(hours=22, minutes=0))))

            ax.set_yticks(np.arange(len(self.activity_set)), labels=self.activity_set)
            ax.set_ylim(-0.5, len(self.activity_set) + 0.5)

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

            return fig, ax

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
