import csv
import datetime
import pytest

from habit_tracker.database import CSVLog, CSVDatabase


@pytest.fixture()
def csv_new_log(tmp_path):
    sample_date = datetime.date(1999, 2, 19)
    return CSVLog.new(sample_date, tmp_path)


@pytest.fixture()
def csv_log(tmp_path):
    sample_date = datetime.date(1999, 2, 19)
    return CSVLog(sample_date, tmp_path)


class TestCSVLog:

    def test_init_instance(self, csv_log):
        # GIVEN a specific parent path and a sample date
        # WHEN creating a CSVLog instance from the constructor
        # THEN the log file is not created yet
        assert not csv_log.exists()

    def test_new_log(self, csv_new_log):
        # GIVEN a specific parent path and a sample date
        # WHEN creating a new file
        # THEN the file is found in the expected path
        assert csv_new_log.exists()

    def test_init_after_log_created(self, tmp_path):
        # GIVEN a specific parent path and a sample date
        sample_date = datetime.date(1999, 2, 19)

        # WHEN creating a new log file
        CSVLog.new(sample_date, tmp_path)

        # AND creating a CSVLog instance from the constructor using the same arguments
        csv_log = CSVLog(sample_date, tmp_path)

        # THEN the instance refers to the file previously created
        assert csv_log.exists()

    def test_new_called_twice(self, tmp_path):
        # GIVEN a specific parent path and a sample date
        sample_date = datetime.date(1999, 2, 19)

        # WHEN creating a new file twice
        CSVLog.new(sample_date, tmp_path)
        CSVLog.new(sample_date, tmp_path)

        # AND creating a CSVLog instance from the constructor using the same arguments
        csv_log = CSVLog(sample_date, tmp_path)

        # THEN the file is found in the expected path
        assert csv_log.exists()

    def test_subfolder_tree_structure(self, csv_new_log):
        # GIVEN a specific parent path and a sample date
        # WHEN getting the parents folders of the log file
        week_folder = csv_new_log._file.parent
        month_folder = week_folder.parent
        year_folder = month_folder.parent

        # THEN the three parent folders get their names from the week, month and year, respectively,
        assert week_folder.name == csv_new_log.week

        # AND the second parent folder is called as the month number from the date
        assert month_folder.name == csv_new_log.month

        # AND the third parent folder is called as the year number from the date
        assert year_folder.name == csv_new_log.year

    def test_create_multiple_instances(self, tmp_path):
        # GIVEN a parent path and two near sample dates
        sample_date1 = datetime.date(1999, 2, 19)
        sample_date2 = datetime.date(1999, 2, 20)

        # WHEN creating two instances of CSVLog
        csv_log1 = CSVLog.new(sample_date1, tmp_path)
        csv_log2 = CSVLog.new(sample_date2, tmp_path)

        # THEN both log files exist
        assert csv_log1.exists()
        assert csv_log2.exists()

    def test_read_file(self, csv_new_log):
        # GIVEN a specific parent path and a sample date
        # WHEN creating a CSVLog instance
        # AND writing a row to its log file
        expected = [
            ["a", "b", "c", "d"],   # First row
            ["e", "f", "g", "h"],   # Second row
        ]
        with open(csv_new_log._file, "a+", newline='') as f:
            writer = csv.writer(f)
            for row in expected:
                writer.writerow(row)

        # AND reading the log file
        actual = csv_new_log.read()

        # THEN the records are retrieved in the same format
        assert expected == actual

    def test_read_empty_file(self, csv_new_log):
        # GIVEN a specific parent path and a sample date
        # WHEN creating a CSVLog instance
        # AND reading the content before adding any content
        # THEN the result obtained is empty
        assert len(csv_new_log.read()) == 0

    def test_update_non_existing_log(self, csv_log):
        # GIVEN a specific parent path, a sample date and sample row
        sample_row = ["sample_activity", "3600", "12:30"]

        # WHEN creating a CSVLog instance from the constructor
        # AND updating the log before creating
        csv_log.update(*sample_row)

        # THEN the file should be created
        assert csv_log.exists()

        # AND the content should be saved as expected
        record = csv_log.read()
        assert record == [sample_row]

    def test_update_one_row(self, csv_new_log):
        # GIVEN a specific parent path and a sample date
        # WHEN creating a CSVLog instance
        # AND updating with a new csv row
        sample_row = ["sample_activity", "3600", "12:30"]
        csv_new_log.update(*sample_row)

        # THEN the content should be saved as expected
        record = csv_new_log.read()
        assert record == [sample_row]

    def test_update_multiple_rows(self, csv_new_log):
        # GIVEN a specific parent path and a sample date
        # WHEN creating a CSVLog instance
        # AND updating with two new csv rows
        sample_row = ["sample_activity1", "3600", "12:30"]
        csv_new_log.update(*sample_row)

        sample_row2 = ["sample_activity2", "1294", "00:49"]
        csv_new_log.update(*sample_row2)

        # THEN the file should save every record appended
        record = csv_new_log.read()
        assert len(record) == 2

        # AND each row should contain the expected content
        assert record == [sample_row, sample_row2]

    def test_update_activity_with_escape(self, csv_new_log):
        sample_row = ["sample\nactivity", "9999", "12:30"]
        csv_new_log.update(*sample_row)
        assert sample_row == csv_new_log.read()[0]

    def test_delete_log(self, csv_new_log):
        # GIVEN a specific parent path and a sample date
        # WHEN creating a CSVLog instance
        # AND deleting the file
        csv_new_log.delete()

        # THEN the file is removed
        assert not csv_new_log.exists()

    def test_delete_non_existing_log(self, csv_log):
        # GIVEN a specific parent path, a sample date and sample row
        # WHEN creating a CSVLog instance from the constructor
        # AND deleting the log file before creating
        csv_log.delete()

        # THEN no error is raised and the file should not exist
        assert not csv_log.exists()

    def test_week_of_month(self, tmp_path):
        # GIVEN a specific parent path and a known date
        sample_date = datetime.date(2023, 5, 28)  # 4th week

        # WHEN creating a CSVLog instance
        csv_log = CSVLog(sample_date, tmp_path)

        # THEN the week is computed as expected
        assert int(csv_log.week) == 4

    def test_day_of_week(self, tmp_path):
        # GIVEN a specific parent path and a known date
        sample_date = datetime.date(2023, 5, 28)  # Sunday

        # WHEN creating a CSVLog instance
        csv_log = CSVLog(sample_date, tmp_path)

        # THEN the day of week is computed as expected
        assert int(csv_log.day_of_week) == 6  # Monday = 0, Sunday = 6


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

