import datetime
import pytest

from habit_tracker.database.csv.log import CSVLog
from habit_tracker.database.csv.database import CSVDatabase


@pytest.fixture()
def csv_db(tmp_path):
    return CSVDatabase(tmp_path)


class TestCSBDatabase:

    def test_read_interval_read_single_log(self, tmp_path):
        # GIVEN a CSV database
        csv_db = CSVDatabase(tmp_path)

        # AND a CSV log with some sample data
        date = datetime.date(2023, 1, 1)
        sample_data = ["sample_activity1", "1", "12:30"]
        csv_log1 = CSVLog(date, tmp_path)
        csv_log1.update(*sample_data)

        # WHEN reading the log related to that dates from the database
        interval_records = csv_db.read_interval(start_date=date)

        # THEN the database retrieves the records from that log in a dictionary
        assert interval_records[date] == [sample_data]

    def test_read_interval_read_single_log_is_empty(self, tmp_path):
        # GIVEN a CSV database
        csv_db = CSVDatabase(tmp_path)

        # AND a CSV log
        date = datetime.date(2023, 1, 1)

        # WHEN reading the log related to that dates from the database
        interval_records = csv_db.read_interval(start_date=date)

        # THEN the database retrieves the empty record in a dictionary
        assert interval_records[date] == []

    def test_read_interval_existing_interval(self, tmp_path):
        # GIVEN a CSV database
        csv_db = CSVDatabase(tmp_path)

        # AND a set of CSV logs about consecutive dates with some sample data
        date1 = datetime.date(2023, 1, 1)
        date2 = date1 + datetime.timedelta(days=1)
        date3 = date2 + datetime.timedelta(days=1)

        sample_data1 = ["sample_activity1", "1", "12:30"]
        sample_data2 = ["sample_activity2", "2", "12:45"]
        sample_data3 = ["sample_activity3", "3", "12:50"]

        csv_log1 = CSVLog(date1, tmp_path)
        csv_log2 = CSVLog(date2, tmp_path)
        csv_log3 = CSVLog(date3, tmp_path)

        csv_log1.update(*sample_data1)
        csv_log2.update(*sample_data2)
        csv_log3.update(*sample_data3)

        # WHEN reading the logs related to those dates from the database
        interval_records = csv_db.read_interval(date1, date3)

        # THEN the database retrieves the records from each log in a dictionary
        assert interval_records[date1] == [sample_data1]
        assert interval_records[date2] == [sample_data2]
        assert interval_records[date3] == [sample_data3]

    def test_read_interval_some_existing_others_not(self, tmp_path):
        # GIVEN a CSV database
        csv_db = CSVDatabase(tmp_path)

        # AND a set of CSV logs about consecutive dates, having some of them some sample data
        date1 = datetime.date(2023, 1, 1)
        date2 = date1 + datetime.timedelta(days=1)
        date3 = date2 + datetime.timedelta(days=1)

        sample_data1 = ["sample_activity1", "1", "12:30"]
        sample_data3 = ["sample_activity3", "3", "12:50"]

        csv_log1 = CSVLog(date1, tmp_path)
        csv_log3 = CSVLog(date3, tmp_path)

        csv_log1.update(*sample_data1)
        csv_log3.update(*sample_data3)

        # WHEN reading the logs related to those dates from the database
        interval_records = csv_db.read_interval(date1, date3)

        # THEN the database retrieves the records from each log in a dictionary as expected
        assert interval_records[date1] == [sample_data1]
        assert interval_records[date2] == []
        assert interval_records[date3] == [sample_data3]

    def test_read_interval_not_valid_dates(self, tmp_path):
        # GIVEN a CSV database
        csv_db = CSVDatabase(tmp_path)

        # AND two different dates
        earlier_date = datetime.date(2023, 1, 1)
        after_date = datetime.date(2023, 1, 10)

        # WHEN trying to read from after_date to earlier_date from the database
        with pytest.warns(UserWarning, match="Not valid interval: end date is earlier than the start date."):
            interval_records = csv_db.read_interval(start_date=after_date, end_date=earlier_date)

        # THEN the database retrieves an empty dictionary and raises a warning.
            assert len(interval_records) == 0
