import datetime

import matplotlib.pyplot as plt
import pytest

from habit_tracker.report import Report


@pytest.fixture()
def report_single_day():
    records = {
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


@pytest.fixture()
def report_multiple_days():
    records = {
        datetime.date(2023, 1, 1): [
            [0, 5000, 34000],
            [1, 6000, 40000],
            [2, 1200, 50000]
        ],
        datetime.date(2023, 1, 2): [
            [0, 8000, 31000],
            [0, 3000, 42000],
            [2, 1200, 50000]
        ],
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
    def test_create_report_from_records(self, report_multiple_days):
        assert isinstance(report_multiple_days, Report)

    def test_total_time_per_activity_single_day(self, report_single_day):
        actual = report_single_day.total_secs_per_activity
        expected = {0: 8400, 1: 3600, 2: 3600}

        assert expected == actual

    def test_total_time_per_activity_multiple_days(self, report_multiple_days):
        actual = report_multiple_days.total_secs_per_activity
        expected = {0: 24400, 1: 9600, 2: 6000}

        assert expected == actual

    def test_plot_seconds_per_activity_single_day(self, report_single_day):
        fig, ax = plt.subplots(1, 1)
        report_single_day.plot_time_per_activity(ax)
        plt.show()

    def test_plot_seconds_per_activity_multiple_days(self, report_multiple_days):
        fig, ax = plt.subplots(1, 1)
        report_multiple_days.plot_time_per_activity(ax)
        plt.show()

    def test_plot_intervals_single_day(self, report_single_day):
        fig, ax = plt.subplots(1, 1, figsize=(14, 4))
        report_single_day.plot_intervals(ax)
        plt.show()

    def test_plot_intervals_multiple_days(self, report_multiple_days):
        fig, ax = plt.subplots(1, 1, figsize=(14, 4))
        report_multiple_days.plot_intervals(ax)
        plt.show()

    def test_plot_report_single_day(self, report_single_day):
        report_single_day.show()

    def test_plot_report_multiple_days(self, report_multiple_days):
        report_multiple_days.show()
