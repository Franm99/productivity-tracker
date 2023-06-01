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

    def options_menu(self, options: list) -> str:
        print(' | '.join(f'{idx}. {item}' for idx, item in enumerate(options)))

        while True:
            ans = input("Choose a number: ")
            try:
                if int(ans) in range(len(options)):
                    break
                else:
                    self.invalid_input(ans)
            except ValueError:
                self.invalid_input(ans)

        return ans

    def confirm(self, message: str) -> bool:
        while True:
            ans = input(f"{message} [y/n]")
            if ans == "y":
                return True
            elif ans == "n":
                return False
            else:
                self.invalid_input(ans)

    def display_selection(self, selection: str) -> None:
        print("->", selection)

    def invalid_input(self, user_input: str) -> None:
        print(f'Input "{user_input}" is not valid. Try again.')

    def wait_input(self, message: str, expected_key: str) -> None:
        while True:
            ans = input(f"{message} [{expected_key}]: ")
            if ans == expected_key:
                break
            else:
                self.invalid_input(ans)
