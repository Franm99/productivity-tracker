from abc import ABC, abstractmethod


class View(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def options_menu(self, message: str, options: list) -> str:
        pass

    @abstractmethod
    def confirm(self, message: str) -> bool:
        pass

    @abstractmethod
    def wait_input(self, message: str, expected_key: str) -> None:
        pass

    @abstractmethod
    def display_selection(self, selection: str) -> None:
        pass

    @abstractmethod
    def invalid_input(self, user_input: str) -> None:
        pass
