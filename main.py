from habit_tracker.tracker import Tracker
from habit_tracker.view import CmdView
from habit_tracker.controller import Controller

import datetime


if __name__ == '__main__':

    tracker = Tracker.create_csv_tracker(datetime.date.today())
    view = CmdView()
    controller = Controller(tracker, view)

    controller.run()
    controller.generate_daily_report()

