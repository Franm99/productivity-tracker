from typing import List


class CmdView:
    def __init__(self):
        pass

    @staticmethod
    def get_new_entry(items: List[str]) -> int:
        options = ' | '.join(f'{idx}. {item}' for idx, item in enumerate(items))
        print(options)
        return int(input("Your choice: "))  # TODO add some filtering

    @staticmethod
    def show_selection(item: str) -> None:
        print("->", item)

    @staticmethod
    def try_again() -> None:
        print("Not valid. Try again.")

    @staticmethod
    def input_to_finish() -> None:
        input("Type anything to finish: ")

    @staticmethod
    def keep_tracking() -> bool:
        while True:
            ans = input("Keep tracking? [y/n]").lower()
            if ans == "y":
                return True
            elif ans == "n":
                return False
            else:
                continue
