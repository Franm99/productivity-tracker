import datetime
import pytest
import re
import time

from habit_tracker.tracker import Tracker
from habit_tracker.report import Report
from habit_tracker.database.csv.database import CSVDatabase


@pytest.fixture()
def tracker_with_csv_db(tmp_path):
    sample_date = datetime.date(1999, 1, 1)
    return Tracker.create_csv_tracker(sample_date, tmp_path)


class TestTrackerWithCSVDatabase:

    def test_create_csv_tracker(self, tracker_with_csv_db):
        # GIVEN a date and a path to save csv logs
        # WHEN creating a tracker object for the given date with a CSV database
        # THEN a Tracker instance is obtained
        isinstance(tracker_with_csv_db, Tracker)

        # AND a CSVDatabase instance is created within the tracker instance
        isinstance(tracker_with_csv_db._db, CSVDatabase)

    def test_start_saves_current_activity(self, tracker_with_csv_db):
        # GIVEN a tracker instance with a CSV database and a sample activity
        sample_activity = "sample_activity"

        # WHEN starting to track an activity
        tracker_with_csv_db.start(sample_activity)

        # THEN the current activity is set to the given activity
        assert tracker_with_csv_db.current_activity == sample_activity

    def test_stop(self, tracker_with_csv_db):
        # GIVEN a tracker instance with a CSV database and a sample activity
        sample_activity = "sample_activity"

        # AND the tracker has been tracking the activity for a while
        tracker_with_csv_db.start(sample_activity)
        time.sleep(1)

        # WHEN stopping the tracking stage
        tracker_with_csv_db.stop()

        # THEN a time interval_seconds has been recorded
        assert tracker_with_csv_db.interval_seconds > 0

        # AND the flag is_tracking is set to False
        assert not tracker_with_csv_db.is_tracking

    def test_stop_before_start(self, tracker_with_csv_db):
        # GIVEN a tracker instance with a CSV database and a sample activity
        # When the tracker stops before been started
        tracker_with_csv_db.stop()

        # THEN an empty time interval_seconds is saved
        assert tracker_with_csv_db.interval_seconds == 0

    def test_add_record_not_fail(self, tracker_with_csv_db):
        # GIVEN a tracker instance with a CSV database and a sample activity
        sample_activity = "sample_activity"

        # AND the tracker starts tracking
        tracker_with_csv_db.start(sample_activity)
        time.sleep(1)

        # WHEN stopping the tracking stage
        tracker_with_csv_db.stop()

        # AND the record is added to the database
        flag = tracker_with_csv_db.add_record()

        # THEN a green flag is returned
        assert flag

    def test_record_saved_on_db(self, tmp_path):
        # GIVEN a tracker instance with a CSV database and a sample activity
        sample_date = datetime.date(1999, 1, 1)
        tracker_with_csv_db = Tracker.create_csv_tracker(sample_date, tmp_path)
        sample_activity = "sample_activity"

        # AND the tracker starts tracking
        tracker_with_csv_db.start(sample_activity)
        time.sleep(1)

        # WHEN stopping the tracking stage
        tracker_with_csv_db.stop()

        # AND the record is added to the database
        tracker_with_csv_db.add_record()

        # THEN the database stores the expected record
        expected = tracker_with_csv_db.record.values()
        actual = tracker_with_csv_db._db.read_log(sample_date)[0]
        assert expected == actual

    def test_add_record_before_stop(self, tracker_with_csv_db):
        # GIVEN a tracker instance with a CSV database and a sample activity
        sample_activity = "sample_activity"

        # AND the tracker starts tracking
        tracker_with_csv_db.start(sample_activity)
        time.sleep(1)

        # WHEN a record is added to the database before stopping track
        flag = tracker_with_csv_db.add_record()

        # THEN a red flag is returned
        assert not flag

    # TODO tests for generate_report() method