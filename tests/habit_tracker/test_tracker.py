import datetime
import pytest
import time

from habit_tracker.tracker import Tracker, Record
from habit_tracker.report import Report
from habit_tracker.database.csv.database import CSVDatabase


@pytest.fixture
def sample_db(tmp_path):
    sample_db_name = "name"
    sample_activity_set = ["a", "bb", "ccc"]
    return CSVDatabase.create(sample_db_name, sample_activity_set, tmp_path)


@pytest.fixture()
def sample_tracker(sample_db):
    sample_date = datetime.date(1999, 1, 1)
    return Tracker(sample_db, sample_date)


class TestTrackerWithCSVDatabase:

    def test_create_tracker(self, sample_tracker):
        # GIVEN a sample CSV-based database and a sample date
        # WHEN creating a tracker instance
        # THEN a Tracker instance is obtained
        isinstance(sample_tracker, Tracker)

        # AND a CSVDatabase instance is linked to the tracker instance
        isinstance(sample_tracker._db, CSVDatabase)

    def test_create_tracker_default_date(self, sample_db):
        # GIVEN a sample CSV-based database
        # WHEN creating a tracker instance without specifying a date
        tracker = Tracker(sample_db)

        # THEN the tracker instance points to the current date
        assert tracker._date == datetime.date.today()

    def test_start_saves_current_activity(self, sample_tracker):
        # GIVEN a tracker instance with a CSV database and the index of a sample activity
        sample_activity_idx = 0

        # WHEN starting to track an activity
        sample_tracker.start(sample_activity_idx)

        # THEN the index of the sample activity is saved as the current activity
        assert sample_tracker._current_activity_idx == sample_activity_idx

    def test_stop(self, sample_tracker):
        # GIVEN a tracker instance with a CSV database and a sample activity
        sample_activity_idx = 0

        # AND the tracker has been tracking the activity for a while
        sample_tracker.start(sample_activity_idx)
        time.sleep(1)

        # WHEN stopping the tracking stage
        sample_tracker.stop()

        # THEN a time interval_seconds has been recorded
        assert sample_tracker._interval_seconds > 0

        # AND the flag is_tracking is set to False
        assert not sample_tracker._is_tracking

    def test_stop_before_start(self, sample_tracker):
        # GIVEN a tracker instance with a CSV database and a sample activity
        # When the tracker stops before been started
        sample_tracker.stop()

        # THEN an empty time interval_seconds is saved
        assert sample_tracker._interval_seconds == 0

    def test_add_record_when_not_tracking(self, sample_tracker):
        # GIVEN a tracker instance with a CSV database and a sample record
        sample_record = Record(activity=0, interval_seconds=10, seconds_from_start=999)

        # WHEN the tracker is not tracking
        sample_tracker._is_tracking = False

        # AND the sample record is added
        flag = sample_tracker.add_record(sample_record)

        # Then the database saves the record.
        expected = sample_tracker._db.read_log(sample_tracker._date)
        assert expected == [sample_record.values()]

        # AND the add_record() method returns True
        assert flag

    def test_add_record_when_tracking(self, sample_tracker):
        # GIVEN a tracker instance with a CSV database and a sample record
        sample_record = Record(activity=0, interval_seconds=10, seconds_from_start=999)

        # WHEN the tracker is tracking
        sample_tracker._is_tracking = True

        # AND the sample record is added
        flag = sample_tracker.add_record(sample_record)

        # Then the database does not save the record.
        expected = sample_tracker._db.read_log(sample_tracker._date)
        assert expected == []

        # AND the add_record() method returns True
        assert not flag

    # TODO tests for generate_report() method
    def test_generate_report_empty_daily_report(self, sample_tracker):
        # GIVEN a tracker instance
        # WHEN trying to generate a daily report for a sample_date with no data
        sample_date = "01-01-1999"
        report = sample_tracker.generate_report(sample_date)

        # THEN a report is obtained
        assert isinstance(report, Report)

    def test_generate_report_not_valid_dates(self, sample_tracker):
        # GIVEN a tracker instance
        # WHEN trying to generate a report for dates in not valid order
        start_date = "30-01-1999"
        end_date = "10-01-1999"
        report = sample_tracker.generate_report(start_date, end_date)

        # THEN a report is obtained
        assert isinstance(report, Report)
