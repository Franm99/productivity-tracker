from typing import Any, Optional
import re

from .view import View


class CliView(View):
    """
    Command line User Interface.
    Recommended to be used while testing.
    """
    def __init__(self):
        """
        Class Constructor.
        """
        super().__init__()

    def options_menu(self, options: list) -> Optional[str]:
        print(' | '.join(f'{idx}. {item}' for idx, item in enumerate(options)))
        self.print_separator()

        while True:
            user_input = input("Choose a number: ")
            try:
                selected_idx = int(user_input)
                if selected_idx in range(len(options)):
                    return options[selected_idx]
                else:
                    self.invalid_input(selected_idx)
            except ValueError:
                self.invalid_input(user_input)

    def confirm(self, message: str) -> bool:
        while True:
            ans = input(f"{message} [y/n]")
            self.print_separator()
            if ans == "y":
                return True
            elif ans == "n":
                return False
            else:
                self.invalid_input(ans)

    def display_selection(self, selection: str) -> None:
        print("->", selection)

    def invalid_input(self, user_input: Any) -> None:
        print(f'Input "{user_input}" is not valid. Try again.')

    def wait_input(self, message: str, expected_key: str) -> None:
        while True:
            ans = input(f"{message} [{expected_key}]: ")
            if ans == expected_key:
                break
            else:
                self.invalid_input(ans)

    def get_list(self, message: str) -> list[str]:
        print(message)
        print("(Press 'q' to finish)")

        items = list()
        end_of_list = False
        while not end_of_list:
            new_item = input(">")

            if new_item == 'q':
                end_of_list = True
            elif new_item in items:
                self.message(f"The activity '{new_item}' is already listed.")
            else:
                items.append(new_item)

        return items

    @staticmethod
    def message(message: str):
        print(message, "\n")

    @staticmethod
    def get_input(message: str = None):
        return input(message)

    def get_input_date(self, message: str = None):
        i = input(message)

        if bool(re.search(r"^(0?[1-9]|[1-2][0-9]|3[0,1])-(0?[1-9]|1[0-2])-(\d{4})$", i)):
            return i
        else:
            self.invalid_input(i)
            return None

    @staticmethod
    def print_separator():
        print("----")
