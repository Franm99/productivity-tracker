import pytest
import datetime

from habit_tracker.controller import Controller, Stage
from habit_tracker.database.csv.database import CSVDatabase
from habit_tracker.tracker import Tracker, Record
from habit_tracker.view.cli import CliView


@pytest.fixture()
def db1(tmp_path):
    return CSVDatabase.create("db1", ["a", "b", "c"], tmp_path)


@pytest.fixture()
def db2(tmp_path):
    return CSVDatabase.create("db2", ["d", "e", "f"], tmp_path)


@pytest.fixture()
def controller_empty_tracker(db1, tmp_path):
    sample_date = datetime.date(1999, 1, 1)
    controller = Controller(CliView(), tmp_path)
    controller.tracker = Tracker(db1, sample_date)
    return controller


@pytest.fixture()
def controller_non_empty_tracker(db1, tmp_path):
    sample_date = datetime.date.today()
    controller = Controller(CliView(), tmp_path)
    controller.tracker = Tracker(db1, sample_date)

    sample_records = [
        Record(activity=0, interval_seconds=7200, seconds_from_start=32400),
        Record(activity=1, interval_seconds=3600, seconds_from_start=41400),
        Record(activity=0, interval_seconds=1200, seconds_from_start=54000),
        Record(activity=2, interval_seconds=3600, seconds_from_start=60000),
    ]

    for record in sample_records:
        controller.tracker.add_record(record)

    return controller


class TestController:

    def test_init_db_directory(self, tmp_path):
        controller = Controller(CliView(), tmp_path)
        assert controller.db_par_dir.exists()

    def test_db_list_no_db(self, tmp_path):
        controller = Controller(CliView(), tmp_path)
        assert len(controller.db_list) == 0

    def test_db_list_one_db(self, db1, tmp_path):
        controller = Controller(CliView(), tmp_path)

        assert len(controller.db_list) == 1
        assert controller.db_list[0] == db1.metadata.name

    def test_db_list_multiple_db(self, db1, db2, tmp_path):
        controller = Controller(CliView(), tmp_path)

        assert len(controller.db_list) == 2
        assert controller.db_list == [db1.metadata.name, db2.metadata.name]

    def test_db_list_db_added_after_init_not_listed(self, tmp_path):
        controller = Controller(CliView(), tmp_path)

        CSVDatabase.create("db1", ["a", "b", "c"], tmp_path)

        assert len(controller.db_list) == 0

    def test_db_list_file_in_db_directory(self, tmp_path):
        sample_file_name = tmp_path / "sample.txt"
        open(sample_file_name, "w").close()

        controller = Controller(CliView(), tmp_path)

        assert sample_file_name.is_file()
        assert len(controller.db_list) == 0

    def test_db_list_empty_directory_in_db_directory(self, tmp_path):
        sample_folder = tmp_path / "sample"
        sample_folder.mkdir()

        controller = Controller(CliView(), tmp_path)

        assert sample_folder.is_dir()
        assert len(controller.db_list) == 0

    def test_stage_select_database_no_db(self, tmp_path):
        controller = Controller(CliView(), tmp_path)

        controller.select_database()

        assert not hasattr(controller.tracker, "_db")
        assert controller.stage == Stage.CreateDatabase

    def test_stage_select_database_multiple_db_valid_selection(self, db1, db2, tmp_path, monkeypatch):
        user_input = iter(["y", 0])
        monkeypatch.setattr('builtins.input', lambda _: next(user_input))

        controller = Controller(CliView(), tmp_path)

        controller.select_database()

        assert controller.tracker._db == db1
        assert controller.stage == Stage.Track

    def test_stage_select_database_multiple_db_no_selection(self, db1, db2, tmp_path, monkeypatch):
        user_input = iter(["n"])
        monkeypatch.setattr('builtins.input', lambda _: next(user_input))

        controller = Controller(CliView(), tmp_path)

        controller.select_database()

        assert not hasattr(controller.tracker, "_db")
        assert controller.stage == Stage.CreateDatabase

    def test_stage_create_database_not_existing(self, tmp_path, monkeypatch):
        user_input = iter(["db1", "a", "b", "c", "q"])
        monkeypatch.setattr('builtins.input', lambda _: next(user_input))

        controller = Controller(CliView(), tmp_path)

        controller.create_database()

        assert controller.tracker._db.name == "db1"
        assert controller.stage == Stage.Track

    def test_stage_create_database_already_exists(self, db1, tmp_path, monkeypatch):
        user_input = iter(["db1"])
        monkeypatch.setattr('builtins.input', lambda _: next(user_input))

        controller = Controller(CliView(), tmp_path)

        controller.create_database()

        assert controller.stage == Stage.CreateDatabase

    def test_stage_track_one_activity_end_tracking(self, controller_empty_tracker, monkeypatch):
        user_input = iter(["0", "q", "n"])
        monkeypatch.setattr('builtins.input', lambda _: next(user_input))

        controller_empty_tracker.track()
        date = controller_empty_tracker.tracker._date
        report = controller_empty_tracker.tracker.generate_report(date)

        assert len(report.records[date]) == 1
        assert controller_empty_tracker.stage == Stage.DailyReport

    def test_stage_track_one_activity_keep_tracking(self, controller_empty_tracker, monkeypatch):
        user_input = iter(["0", "q", "y"])
        monkeypatch.setattr('builtins.input', lambda _: next(user_input))

        controller_empty_tracker.track()
        date = controller_empty_tracker.tracker._date
        report = controller_empty_tracker.tracker.generate_report(date)

        print(report.records)
        assert len(report.records[date]) == 1
        assert controller_empty_tracker.stage == Stage.Track

    def test_stage_daily_report_show_today_report(self, controller_non_empty_tracker, monkeypatch):
        user_input = iter(["y"])
        monkeypatch.setattr('builtins.input', lambda _: next(user_input))

        controller_non_empty_tracker.show_daily_reports()

        assert controller_non_empty_tracker.stage == Stage.OtherReports

    def test_stage_daily_report_not_show_daily_report(self, controller_non_empty_tracker, monkeypatch):
        user_input = iter(["n"])
        monkeypatch.setattr('builtins.input', lambda _: next(user_input))

        controller_non_empty_tracker.show_daily_reports()

        assert controller_non_empty_tracker.stage == Stage.OtherReports



