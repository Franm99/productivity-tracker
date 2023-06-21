from habit_tracker.view.cli import CliView
from habit_tracker.controller import Controller


if __name__ == '__main__':

    view = CliView()
    controller = Controller(view)

    controller.run()
