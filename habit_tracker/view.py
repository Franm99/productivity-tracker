from typing import List


class CmdView:
    """
    Command line User Interface.
    Recommended to be used while testing.
    """
    def __init__(self):
        """
        Class Constructor.
        """
        pass

    @staticmethod
    def get_new_entry(items: List[str]) -> int:
        """
        Expects the user to select one option.
        :param items: list of possible items to select
        :return: Selected item.
        """
        options = ' | '.join(f'{idx}. {item}' for idx, item in enumerate(items))
        print(options)
        return int(input("Your choice: "))  # TODO add some filtering

    @staticmethod
    def show_selection(item: str) -> None:
        """
        Displays the selected item.
        :param item: item to display
        :return: None
        """
        print("->", item)

    @staticmethod
    def try_again() -> None:
        """
        Tells the user to give a new entry.
        :return: None
        """
        print("Not valid. Try again.")

    @staticmethod
    def input_to_finish() -> None:
        """
        Expects the user to type something for the program to keep running.
        :return: None
        """
        input("Type anything to finish: ")

    @staticmethod
    def keep_tracking() -> bool:
        """
        Asks the user for a new entry or to finish.
        :return:
        """
        while True:
            ans = input("Keep tracking? [y/n]").lower()
            if ans == "y":
                return True
            elif ans == "n":
                return False
            else:
                continue
