import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import numpy as np
import datetime


class Graphics:
    plt.style.use('seaborn-v0_8-darkgrid')

    def __init__(self):
        fig, axes = plt.subplots(1, 2, figsize=(14, 3), gridspec_kw={'width_ratios': [1, 3]})
        self.fig: plt.Figure = fig
        self.ax1: plt.axis = axes[0]
        self.ax2: plt.axis = axes[1]

    def pie(self, x, labels: list[str], autopct=None, wedgeprops=None):
        self.ax1.pie(x, labels=labels, autopct=autopct, wedgeprops=wedgeprops)

    def workday(self, records: dict, activity_set):
        dates = list(records.keys())
        if not dates:
            return None
        else:
            base_dt = dates[0]
            base_date = datetime.datetime.combine(base_dt, datetime.datetime.min.time())

            self.ax2.set_xlim((np.datetime64(str(base_date + datetime.timedelta(hours=6))),
                               np.datetime64(str(base_date + datetime.timedelta(hours=22)))))

            self.ax2.set_yticks(np.array(list(range(len(activity_set)))), labels=activity_set)
            self.ax2.set_ylim(-0.5, 2.5)

            locator = mdates.HourLocator(interval=1)
            formatter = mdates.DateFormatter('%H:%M')

            self.ax2.xaxis.set_major_locator(locator)
            self.ax2.xaxis.set_major_formatter(formatter)

            for daily_records in records.values():
                intervals = self.compute_intervals(daily_records, base_date)

                for label in intervals:
                    y = [int(label)] * 2
                    for interval in intervals[label]:
                        self.discrete_interval(interval, y, ax=self.ax2, linewidth=25, solid_capstyle='butt',
                                               color=(0.2, 0.2, 0.2, 0.2))

    @staticmethod
    def show():
        plt.show()

    @staticmethod
    def discrete_interval(x, y, ax=None, where='post', **kwargs):
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
