import datetime

import matplotlib.pyplot as plt
import pytest

from habit_tracker.report import Report


@pytest.fixture()
def sample_report():
    records = {
        datetime.date(2023, 1, 1): [
            [0, 100, 0],
            [1, 200, 100],
            [2, 300, 300]
        ],
        datetime.date(2023, 1, 2): [],
        datetime.date(2023, 1, 3): [
            [0, 7200, 32400],
            [1, 3600, 41400],
            [0, 1200, 54000],
            [2, 3600, 60000]
        ]
    }

    activity_set = [
        "activity1",
        "activity2",
        "activity3"
    ]

    return Report(records, activity_set)


class TestReport:
    def test_create_report_from_records(self, sample_report):
        assert isinstance(sample_report, Report)

    def test_daily_records_per_activity(self, sample_report):
        sample_date = datetime.date(2023, 1, 3)  # Contains multiple records for the same activity

        actual = sample_report.daily_hours_per_activity(sample_date)
        expected = {0: 8400, 1: 3600, 2: 3600}

        assert expected == actual

    def test_daily_records_per_activity_day_with_no_records(self, sample_report):
        sample_date = datetime.date(2023, 1, 2)

        actual = sample_report.daily_hours_per_activity(sample_date)
        expected = dict()

        assert expected == actual

    def test_daily_records_per_activity_non_registered_day(self, sample_report):
        sample_date = datetime.date(2023, 1, 4)

        actual = sample_report.daily_hours_per_activity(sample_date)
        expected = dict()

        assert expected == actual

    def test_plot_time_per_activity(self, sample_report):
        # TODO needs manual interaction. Find a better way to test.
        sample_date = datetime.date(2023, 1, 3)
        sample_report.plot_time_per_activity(sample_date)
        plt.show()

    def test_plot_intervals_in_day(self, sample_report):
        # TODO needs manual interaction. Find a better way to test.
        sample_date = datetime.date(2023, 1, 3)
        sample_report.plot_intervals_in_day(sample_date)
        plt.show()
