from habit_tracker.view.cli import CliView
from habit_tracker.controller import Controller


if __name__ == '__main__':

    # tracker = Tracker.create_csv_tracker(datetime.date.today())
    view = CliView()
    controller = Controller(view)

    controller.run()
