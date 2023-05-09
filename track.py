import matplotlib.pyplot as plt
import os

from csv import DictWriter, reader
from datetime import date, timedelta
from enum import Enum
from time import time
from typing import Tuple, Optional

LOGS_FOLDER = "daily_logs"


class ACTION(Enum):
    PROJECT = 0
    COURSE = 1
    HOUSE = 2  # Involves: cat, householding chores, shopping, cooking, etc.
    REST = 3


def start(tag: int) -> Optional[str]:
    try:
        return ACTION(tag).name
    except ValueError:
        return None


def stop() -> float:
    input("Write something to finish.")
    return time()


def track_performance() -> Tuple[str, int]:
    options = ' | '.join(f'{key}: {value}' for key, value in zip([e.name for e in ACTION], [e.value for e in ACTION]))
    print(options)

    task = None
    while not task:
        choice = int(input("-> "))
        task = start(choice)
        if not task:
            print("Not valid. Try again.")

    time_start = time()
    input("Type anything to finish: ")
    interval = round(time() - time_start)
    return task, interval


def save_action(file: str, action: str, interval: int) -> None:
    with open(file, "a+", newline='') as f:
        fieldnames = ["action", "interval"]
        writer = DictWriter(f, fieldnames=fieldnames)
        writer.writerow({"action": action, "interval": interval})


def compute_totals(file: str) -> dict:
    records = dict()
    with open(file, "r") as f:
        csv_reader = reader(f, delimiter=",")
        for row in csv_reader:
            records[row[0]] = int(row[1]) + records.get(row[0], 0)
    return records


def show_results(records: dict):
    plt.figure()
    seconds_spent = sum(records.values())

    def autopct_format(pctg):
        value = timedelta(seconds=round(seconds_spent * pctg / 100))
        return f'{pctg:.2f}%\n({value})'

    plt.pie(records.values(), labels=records.keys(), autopct=autopct_format,
            wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'})
    plt.title(str(date.today()))
    plt.tight_layout()
    plt.show()
    # todo: Create plot x-y - time-action


if __name__ == "__main__":
    current_date = str(date.today())

    if not os.path.exists(LOGS_FOLDER):
        os.makedirs(LOGS_FOLDER)

    filename = f"{LOGS_FOLDER}/{current_date}.csv"

    finish = False
    while not finish:
        task, time_spent = track_performance()
        save_action(filename, task, time_spent)

        i = input("Keep tracking? [y/n]").lower()
        while i not in ("y", "n"):
            i = input("Keep tracking? [y/n]").lower()
        finish = True if i == "n" else False

    totals = compute_totals(filename)
    show_results(totals)






