from enum import Enum, auto

from .tracker import Tracker
from .database.csv.database import CSVDatabase
from .view.cli import CliView

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
                self.show_history_report()

        self.end_program()

    def select_database(self):
        self.gui.section_intro("Choose Database")
        if not self.db_list:
            self.gui.message("No databases found.")
            self.stage = Stage.CreateDatabase
            return

        else:
            load_db = self.gui.confirm(f'{len(self.db_list)} existing database(s) found. Load?')

            if load_db:
                selected = self.gui.options_menu("Choose your database", self.db_list)
                self.gui.message(f'Loading database: {selected}')
                db = CSVDatabase.load_from_name(selected, self.db_par_dir)
            else:
                self.stage = Stage.CreateDatabase
                return

        self.tracker = Tracker(db)
        self.stage = Stage.Track

    def create_database(self):
        self.gui.section_intro("Create a new Database")
        db_name = self.gui.get_input("Choose a name")
        if db_name in self.db_list:
            self.gui.message(f'The name "{db_name}" is already used. Try another one.')
            self.stage = Stage.CreateDatabase

        else:
            activities_list = self.gui.get_list("Type a list of activities to track.")
            db = CSVDatabase.create(db_name, activities_list, self.db_par_dir)

            self.tracker = Tracker(db)
            self.stage = Stage.Track

    def track(self):
        self.gui.print_separator()
        self.ask_new_entry()
        self.wait()
        if not self.gui.confirm("Track a new activity?"):
            self.stage = Stage.DailyReport
            self.save_reports()
        else:
            self.stage = Stage.Track

    def ask_new_entry(self) -> None:
        """
        Tells to the view to ask the user for a new activity to track.
        :return: None
        """
        activity_set = self.tracker.activity_set
        current_activity = self.gui.options_menu("Choose an activity to track", activity_set)
        activity_idx = activity_set.index(current_activity)

        self.gui.display_selection(current_activity)
        self.tracker.start(activity_idx)

    def wait(self) -> None:
        """
        Wait for event to trigger the end of the tracking stage for the current activity.
        :return: None
        """
        self.gui.wait_input("Do your best!", "q")  # TODO add a random message
        self.tracker.stop()

    def show_daily_reports(self):
        self.gui.section_intro("Show reports")
        if self.gui.confirm("Show today's report?"):
            self.gui.message("Close the popup window to proceed...")
            report = self.tracker.generate_report(start_date='today')
            report.show()
            report.graphics.fig.savefig("sample")

        self.stage = Stage.OtherReports

    def show_history_report(self):
        if self.gui.confirm("Show your history?"):
            # Ask start and end date
            start_date, end_date = None, None
            while not start_date:
                start_date = self.gui.get_input_date("> Start Date [dd-mm-yyyy]: ")
            while not end_date:
                end_date = self.gui.get_input_date("> End date [dd-mm-yyyy]: ")

            self.gui.message("Close the popup window to proceed...")
            report = self.tracker.generate_report(start_date, end_date)
            report.show()

        self.stage = Stage.End

    def save_reports(self):
        pass

    def end_program(self):
        pass
