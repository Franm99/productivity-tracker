from .tracker import Tracker
from .view import CmdView
from .utils import Activity, ReportType


class Controller:
    def __init__(self, model: Tracker, view: CmdView):
        self.tracker = model
        self.ui = view

    def run(self):
        # TODO: This workflow is thought for only daily reports. Refactor.
        while True:
            self.ask_new_entry()
            self.ui.show_selection(self.tracker.current_activity)

            self.wait()
            self.tracker.add_track()

            if not self.ui.keep_tracking():
                break

    def generate_daily_report(self):
        report = self.tracker.generate_report(ReportType.DAY)
        report.compute_totals()
        report.show()

    def ask_new_entry(self):
        activities = [a.name for a in Activity]
        current_activity = self.ui.get_new_entry(activities)
        self.tracker.start(Activity(current_activity).name)

    def wait(self):
        self.ui.input_to_finish()
        self.tracker.stop()
