from habit_tracker.tracker import Tracker
from habit_tracker.view.cli import CliView
from habit_tracker.controller import Controller

import datetime


if __name__ == '__main__':

    tracker = Tracker.create_csv_tracker(datetime.date.today())
    view = CliView()
    controller = Controller(tracker, view)

    controller.run()
    controller.generate_daily_report()

