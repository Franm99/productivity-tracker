import csv
import datetime
import pytest

from habit_tracker.database.csv.log import CSVLog


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
        assert week_folder.name == csv_new_log._week

        # AND the second parent folder is called as the month number from the date
        assert month_folder.name == csv_new_log._month

        # AND the third parent folder is called as the year number from the date
        assert year_folder.name == csv_new_log._year

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
            ["a", "b", "c.txt", "d"],   # First row
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
        assert int(csv_log._week) == 4

    def test_day_of_week(self, tmp_path):
        # GIVEN a specific parent path and a known date
        sample_date = datetime.date(2023, 5, 28)  # Sunday

        # WHEN creating a CSVLog instance
        csv_log = CSVLog(sample_date, tmp_path)

        # THEN the day of week is computed as expected
        assert int(csv_log._day_of_week) == 6  # Monday = 0, Sunday = 6
