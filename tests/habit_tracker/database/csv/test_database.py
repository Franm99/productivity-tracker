import datetime
import pytest

from habit_tracker.database.csv.log import CSVLog
from habit_tracker.database.csv.database import CSVDatabase
from habit_tracker.database.csv.metadata import DBMetadata


@pytest.fixture()
def sample_metadata(tmp_path):
    kwargs = {
        "name": "sample_db",
        "activities": ["a", "bb", "ccc"],
        "par_dir": tmp_path
    }
    return DBMetadata(**kwargs)


@pytest.fixture()
def sample_db(tmp_path):
    sample_name = "name"
    sample_activity_set = ["a", "bb", "ccc"]
    return CSVDatabase.create(sample_name, sample_activity_set, tmp_path)


class TestCSBDatabase:

    def test_init_from_metadata(self, sample_metadata, tmp_path):
        db = CSVDatabase(sample_metadata)
        assert isinstance(db.metadata, DBMetadata)

    def test_create_new_db(self, tmp_path):
        sample_name = 'name'
        sample_activity_set = ['a', 'bb', 'ccc']
        db = CSVDatabase.create(sample_name, sample_activity_set, tmp_path)
        assert (tmp_path / db.metadata.db_path).is_dir()
        assert (tmp_path / db.metadata.file).is_file()

    def test_load_from_name_not_found(self, tmp_path):
        sample_name = 'name'
        db = CSVDatabase.load_from_name(sample_name, tmp_path)
        assert not isinstance(db, CSVDatabase)

    def test_load_from_name_existing_db(self, tmp_path):
        sample_name = 'name'
        sample_activity_set = ['a', 'bb', 'ccc']
        CSVDatabase.create(sample_name, sample_activity_set, tmp_path)
        db = CSVDatabase.load_from_name(sample_name, tmp_path)
        assert isinstance(db, CSVDatabase)

    def test_read_interval_read_single_log(self, sample_db):
        # GIVEN a CSV database
        # AND a CSV log with some sample data
        date = datetime.date(2023, 1, 1)
        sample_data = ["sample_activity1", "1", "12:30"]
        csv_log1 = CSVLog(date, base_dir=sample_db.metadata.db_path)
        csv_log1.update(*sample_data)

        # WHEN reading the log related to that date from the database
        interval_records = sample_db.read_interval(start_date=date)

        # THEN the database retrieves the records from that log in a dictionary
        assert interval_records[date] == [sample_data]

    def test_read_interval_read_single_log_is_empty(self, sample_db):
        # GIVEN a CSV database with no logs
        # AND a sample date
        date = datetime.date(2023, 1, 1)

        # WHEN reading the log related to that date from the database
        interval_records = sample_db.read_interval(start_date=date)

        # THEN the database retrieves an empty record in a dictionary
        assert interval_records[date] == []

    def test_read_interval_existing_interval(self, sample_db):
        # GIVEN a CSV database
        # AND a set of CSV logs about consecutive dates with some sample data
        date1 = datetime.date(2023, 1, 1)
        date2 = date1 + datetime.timedelta(days=1)
        date3 = date2 + datetime.timedelta(days=1)

        sample_data1 = ["sample_activity1", "1", "12:30"]
        sample_data2 = ["sample_activity2", "2", "12:45"]
        sample_data3 = ["sample_activity3", "3", "12:50"]

        csv_log1 = CSVLog(date1, base_dir=sample_db.metadata.db_path)
        csv_log2 = CSVLog(date2, base_dir=sample_db.metadata.db_path)
        csv_log3 = CSVLog(date3, base_dir=sample_db.metadata.db_path)

        csv_log1.update(*sample_data1)
        csv_log2.update(*sample_data2)
        csv_log3.update(*sample_data3)

        # WHEN reading the logs related to those dates from the database
        interval_records = sample_db.read_interval(date1, date3)

        # THEN the database retrieves the records from each log in a dictionary
        assert interval_records[date1] == [sample_data1]
        assert interval_records[date2] == [sample_data2]
        assert interval_records[date3] == [sample_data3]

    def test_read_interval_some_existing_others_not(self, sample_db):
        # GIVEN a CSV database
        # AND a set of CSV logs about consecutive dates, having some of them some sample data
        date1 = datetime.date(2023, 1, 1)
        date2 = date1 + datetime.timedelta(days=1)
        date3 = date2 + datetime.timedelta(days=1)

        sample_data1 = ["sample_activity1", "1", "12:30"]
        sample_data3 = ["sample_activity3", "3", "12:50"]

        csv_log1 = CSVLog(date1, base_dir=sample_db.metadata.db_path)
        csv_log3 = CSVLog(date3, base_dir=sample_db.metadata.db_path)

        csv_log1.update(*sample_data1)
        csv_log3.update(*sample_data3)

        # WHEN reading the logs related to those dates from the database
        interval_records = sample_db.read_interval(date1, date3)

        # THEN the database retrieves the records from each log in a dictionary as expected
        assert interval_records[date1] == [sample_data1]
        assert interval_records[date2] == []
        assert interval_records[date3] == [sample_data3]

    def test_read_interval_not_valid_dates(self, sample_db):
        # GIVEN a CSV database
        # AND two different dates
        earlier_date = datetime.date(2023, 1, 1)
        after_date = datetime.date(2023, 1, 10)

        # WHEN trying to read from after_date to earlier_date from the database
        with pytest.warns(UserWarning, match="Not valid interval_seconds: end date is earlier than the start date."):
            interval_records = sample_db.read_interval(start_date=after_date, end_date=earlier_date)

        # THEN the database retrieves an empty dictionary and raises a warning.
            assert len(interval_records) == 0
