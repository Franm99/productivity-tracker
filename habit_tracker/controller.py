from .tracker import Tracker
from .view import CmdView
from .utils import Activity

import datetime


class Controller:
    """ The controller communicates the View (UI) with the Model (Tracker)."""
    def __init__(self, model: Tracker, view: CmdView):
        """
        Class Constructor.
        :param model: model object implementing the business logic of the application.
        :param view: User interface object implementing methods to communicate with the user.
        """
        self.tracker = model
        self.gui = view

    def run(self) -> None:
        """
        Executes the application main loop to start to listen to events from the view and the model.
        :return: None
        """
        # TODO: This workflow is thought for only daily reports. Refactor.
        while True:
            self.ask_new_entry()
            self.gui.show_selection(self.tracker.current_activity)

            self.wait()
            self.tracker.add_record()

            if not self.gui.keep_tracking():
                break

    def generate_daily_report(self) -> None:
        """
        Generate Daily report based on current data.
        :return: None
        """
        report = self.tracker.generate_report(datetime.date.today())
        report.daily_time_per_activity()
        report.show()

    def ask_new_entry(self) -> None:
        """
        Tells to the view to ask the user for a new activity to track.
        :return: None
        """
        activities = [a.name for a in Activity]
        current_activity = self.gui.get_new_entry(activities)
        self.tracker.start(Activity(current_activity).name)

    def wait(self) -> None:
        """
        Wait for event to trigger the end of the tracking stage for the current activity.
        :return: None
        """
        self.gui.input_to_finish()
        self.tracker.stop()
