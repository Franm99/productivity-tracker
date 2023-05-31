import datetime
import matplotlib.pyplot as plt

# TODO Complete refactor


class Report:
    def __init__(self, records: dict[datetime.date]):
        self.records = records
        self.daily_records = dict()

    def daily_time_per_activity(self, date: datetime.date = None):
        date = date if date else datetime.date.today()
        for daily_records in self.records[date]:
            self.daily_records[daily_records[0]] = int(daily_records[1]) + self.daily_records.get(daily_records[0], 0)

    def show(self, date: datetime.date = None):
        date = date if date else datetime.date.today()
        plt.figure()
        seconds_spent = sum(self.daily_records.values())

        def autopct_format(pctg):
            value = datetime.timedelta(seconds=round(seconds_spent * pctg / 100))
            return f'{pctg:.2f}%\n({value})'

        plt.pie(self.daily_records.values(), labels=self.daily_records.keys(), autopct=autopct_format,
                wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'})
        plt.title(date)
        plt.tight_layout()
        plt.show()
