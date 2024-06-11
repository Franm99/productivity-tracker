from typing import Any, Optional
import re
import logging
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich import print, style
from rich.prompt import Prompt, Confirm
from .view import View
from rich.progress import Progress, TimeElapsedColumn, SpinnerColumn


logger = logging.getLogger(__name__)


class CliView(View):
    """
    Command line User Interface.
    Recommended to be used while testing.
    """
    def __init__(self):
        """
        Class Constructor.
        """
        logger.debug("VIEW: Command line interface")
        super().__init__()
        self.console = Console(force_terminal=True)

    def options_menu(self, message: str, options: list) -> Optional[str]:
        logger.info("Printing list of options.")
        self.console.print(
            Panel(
                Columns(options, expand=True, align='center', padding=(0, 0)),
                title=message,
            )
        )
        return Prompt.ask(choices=options, show_choices=False)

    def confirm(self, message: str) -> bool:
        return Confirm.ask(message)

    def display_selection(self, selection: str) -> None:
        print(f"Currently doing -> [bold italic green]{selection}[/bold italic green]")

    def invalid_input(self, user_input: Any) -> None:
        logger.info(f'Invalid user input: {user_input}.')
        print(f'Input "{user_input}" is not valid. Try again.')

    def wait_input(self, message: str, expected_key: str) -> None:
        logger.info('Waiting for user input to end wait loop.')

        with self.console.status("Press enter to finish", spinner="simpleDots"):
            input()

        logger.info('Exit from wait loop.')

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

    def section_intro(self, message: str):
        self.console.rule(
            f"[bold green]{message}[/bold green]",
            characters='=',
            style=style.Style(
                color='green',
                bold=True,
            )
        )

    @staticmethod
    def get_input(message: str = None):
        return input(f"{message} -> ")

    def get_input_date(self, message: str = None):
        i = input(message)

        if bool(re.search(r"^(0?[1-9]|[1-2][0-9]|3[0,1])-(0?[1-9]|1[0-2])-(\d{4})$", i)):
            return i
        else:
            self.invalid_input(i)
            return None

    def print_separator(self):
        self.console.rule()
