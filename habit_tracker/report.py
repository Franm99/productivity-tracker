import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# TODO Complete refactor


class Report:
    def __init__(self, records: dict[datetime.date]):
        self.records = records
        self.daily_records = dict()

        plt.style.use('seaborn-v0_8-darkgrid')

    def daily_time_per_activity(self, date: datetime.date = None):
        date = date if date else datetime.date.today()
        for daily_records in self.records[date]:
            self.daily_records[daily_records[0]] = int(daily_records[1]) + self.daily_records.get(daily_records[0], 0)

    def show(self, date: datetime.date = None):

        date = date if date else datetime.date.today()
        self.plot_pie(date)
        self.plot_day(date)
        plt.show()

    def plot_pie(self, date: datetime.date):
        fig, ax = plt.subplots(1, 1)
        seconds_spent = sum(self.daily_records.values())

        def autopct_format(pctg):
            value = datetime.timedelta(seconds=round(seconds_spent * pctg / 100))
            return f'{pctg:.2f}%\n({value})'

        ax.pie(self.daily_records.values(), labels=self.daily_records.keys(), autopct=autopct_format,
                wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'})
        ax.set_title(date)
        fig.tight_layout()

    def plot_day(self, date: datetime.date):
        base_dt = datetime.datetime.combine(date, datetime.datetime.min.time())

        labels = self.dict_from_names(date)

        fig, ax = plt.subplots(1, 1, figsize=(14, 5))
        ax.set_xlim(np.datetime64(str(base_dt + datetime.timedelta(hours=8, minutes=30))),
                    np.datetime64(str(base_dt + datetime.timedelta(hours=9, minutes=6))))

        ax.set_yticks(np.array(list(labels.values())), labels=list(labels.keys()))
        ax.set_ylim(min(labels.values()) - 0.5, max(labels.values()) + 0.5)

        locator = mdates.AutoDateLocator(minticks=12, maxticks=24)
        formatter = mdates.ConciseDateFormatter(locator)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)

        intervals = dict()
        for record in self.records[date]:
            start = base_dt + datetime.timedelta(seconds=int(record[2]))
            end = start + datetime.timedelta(seconds=int(record[1]))

            if record[0] not in intervals:
                intervals[record[0]] = [[start, end]]
            else:
                intervals[record[0]].append([start, end])

        for label in intervals:
            y = [labels[label]] * 2
            for interval in intervals[label]:
                x = interval
                self.my_step(x, y, linewidth=25, solid_capstyle='butt', color='blue')

    def dict_from_names(self, date: datetime.date = None):
        names = dict()
        counter = 0
        if date in self.records:
            for record in self.records[date]:
                if record[0] not in names:
                    names[record[0]] = counter
                    counter += 1
        return names

    @staticmethod
    def my_step(x, y, ax=None, where='post', **kwargs):
        assert where in ['post', 'pre']
        x = np.array(x)
        y = np.array(y)

        y_slice = y[:-1] if where == 'post' else y[1:]

        X = np.c_[x[:-1], x[1:], x[1:]]
        Y = np.c_[y_slice, y_slice, np.zeros_like(x[:-1]) * np.nan]

        if not ax:
            ax = plt.gca()

        return ax.plot(X.flatten(), Y.flatten(), **kwargs)
