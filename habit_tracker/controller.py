from enum import Enum, auto

from .tracker import Tracker
from .database.csv.database import CSVDatabase
from .view.cli import CliView

import datetime
import pathlib

DEF_DB_PAR_DIR = pathlib.Path('.db')


class Stage(Enum):
    SelectDatabase = auto()
    CreateDatabase = auto()
    Track = auto()
    DailyReport = auto()
    OtherReports = auto()
    End = auto()


class Controller:
    """ The controller communicates the View (UI) with the Model (Tracker)."""
    def __init__(self, view: CliView, db_par_dir: pathlib.Path = None):
        self.tracker = None
        self.gui = view
        self.db_par_dir: pathlib.Path = db_par_dir if db_par_dir else DEF_DB_PAR_DIR

        if not self.db_par_dir.exists():
            self.db_par_dir.mkdir(parents=True)

        self.db_list = self.find_databases()  # TODO: db's created after init are not listed here

        self.stage = Stage.SelectDatabase

    def find_databases(self) -> list[str]:
        db_list = []
        db_par_dir_items = self.db_par_dir.iterdir()
        for item in db_par_dir_items:
            if item.is_dir() and (item / "metadata.json").is_file():
                db_list.append(item.name)
        return db_list

    def run(self) -> None:
        """
        Executes the application main loop to start to listen to events from the view and the model.
        :return: None
        """
        while self.stage != Stage.End:
            if self.stage == Stage.SelectDatabase:
                self.select_database()
            if self.stage == Stage.CreateDatabase:
                self.create_database()
            if self.stage == Stage.Track:
                self.track()
            if self.stage == Stage.DailyReport:
                self.show_daily_reports()
            if self.stage == Stage.OtherReports:
                self.show_interval_report()

        self.end_program()

    def select_database(self):

        if not self.db_list:
            self.gui.message("No databases found.")
            self.stage = Stage.CreateDatabase
            return

        else:
            load_db = self.gui.confirm(f'{len(self.db_list)} existing database(s) found. Load?')

            if load_db:
                selected = self.gui.options_menu(self.db_list)
                self.gui.message(f'Loading database: {selected}')
                db = CSVDatabase.load_from_name(selected, self.db_par_dir)

            else:
                self.stage = Stage.CreateDatabase
                return

        self.tracker = Tracker(db)
        self.stage = Stage.Track

    def create_database(self):
        db_name = self.gui.get_input("Choose a name for your habit tracker.")
        if db_name in self.db_list:
            self.gui.message(f'The name "{db_name}" is already used. Try another one.')
            self.stage = Stage.CreateDatabase

        else:
            activities_list = self.gui.get_list("Type a list of activities to track.")
            db = CSVDatabase.create(db_name, activities_list, self.db_par_dir)

            self.tracker = Tracker(db)
            self.stage = Stage.Track

    def track(self):
        self.ask_new_entry()
        self.wait()
        if not self.gui.confirm("Track a new activity?"):
            self.stage = Stage.DailyReport
        else:
            self.stage = Stage.Track

    def ask_new_entry(self) -> None:
        """
        Tells to the view to ask the user for a new activity to track.
        :return: None
        """
        activity_set = self.tracker.activity_set
        current_activity = self.gui.options_menu(activity_set)
        activity_idx = activity_set.index(current_activity)

        self.gui.display_selection(current_activity)
        self.tracker.start(activity_idx)

    def wait(self) -> None:
        """
        Wait for event to trigger the end of the tracking stage for the current activity.
        :return: None
        """
        self.gui.wait_input("Type to finish", "q")
        self.tracker.stop()

    def show_daily_reports(self):
        if self.gui.confirm("Show today's report?"):
            report = self.tracker.generate_report(datetime.date.today())
            report.show()

        self.stage = Stage.OtherReports

    def show_history_report(self):
        if self.gui.confirm("Show your history?"):
            # TODO complete
            pass
        self.stage = Stage.End

    def end_program(self):
        pass
