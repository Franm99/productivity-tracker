import datetime

# TODO complete


class Report:
    def __init__(self, records: dict[datetime.date]):
        self.records = records

    def compute_time_per_activity(self):
        pass

# class DailyReport(Report):
#     """ Daily report. """
#     def __init__(self, date):
#         """
#         Class Constructor.
#         :param db: Database to take records from.
#         """
#         super().__init__()
#         self._db = db
#         self._date = db.file_path.stem
#         self.records = dict()
#
#     def compute_time_per_activity(self) -> None:
#         """
#         Reads records from the database and gathers them based on the type of activity.
#         :return: None
#         """
#         records = self._db.read()
#         for record in records:
#             self.records[record[0]] = int(record[1]) + self.records.get(record[0], 0)
#
#     def show(self) -> None:
#         """
#         Create plots to show results to the user.
#         # TODO refactor, decouple and divide in tasks.
#         :return: None
#         """
#         plt.figure()
#         seconds_spent = sum(self.records.values())
#
#         def autopct_format(pctg):
#             value = timedelta(seconds=round(seconds_spent * pctg / 100))
#             return f'{pctg:.2f}%\n({value})'
#
#         plt.pie(self.records.values(), labels=self.records.keys(), autopct=autopct_format,
#                 wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'})
#         plt.title(self._date)
#         plt.tight_layout()
#         plt.show()
#
#     def plot_pie_chart(self):
#         pass
#
#     def plot_day_chart(self):
#         pass
