import pytest

from habit_tracker.view.cli import CliView


@pytest.fixture
def gui():
    return CliView()


@pytest.fixture
def options_list():
    return ["option1", "option2", "option3"]


class TestCliView:

    def test_options_menu_correct_option_index(self, gui, options_list, monkeypatch):
        expected = "option1"
        monkeypatch.setattr('builtins.input', lambda _: 0)

        actual = gui.options_menu(options_list)
        assert expected == actual

    def test_options_menu_input_not_a_number(self, gui, options_list, monkeypatch):
        expected_inputs = iter(["a", 0])
        monkeypatch.setattr('builtins.input', lambda _: next(expected_inputs))

        expected = "option1"

        actual = gui.options_menu(options_list)
        assert expected == actual

    def test_options_menu_input_index_out_of_range(self, gui, options_list, monkeypatch):
        expected_inputs = iter([4, 0])
        monkeypatch.setattr('builtins.input', lambda _: next(expected_inputs))

        expected = "option1"

        actual = gui.options_menu(options_list)
        assert expected == actual

    def test_options_menu_multiple_not_valid_inputs(self, gui, options_list, monkeypatch):
        expected_inputs = iter(["b", 3, "option1", 0])
        monkeypatch.setattr('builtins.input', lambda _: next(expected_inputs))

        expected = "option1"

        actual = gui.options_menu(options_list)
        assert expected == actual

    def test_confirm_yes(self, gui, monkeypatch):
        sample_question = "sample question?"
        expected_input = "y"
        monkeypatch.setattr('builtins.input', lambda _: expected_input)

        expected = True

        actual = gui.confirm(sample_question)
        assert expected == actual

    def test_confirm_no(self, gui, monkeypatch):
        sample_question = "sample question?"
        expected_input = "n"
        monkeypatch.setattr('builtins.input', lambda _: expected_input)

        expected = False

        actual = gui.confirm(sample_question)
        assert expected == actual

    def test_confirm_multiple_not_valid_inputs(self, gui, monkeypatch):
        sample_question = "sample question?"
        expected_inputs = iter(["yes", "Y", "YES", "no", "N", "NO", "q", "other", "y"])
        monkeypatch.setattr('builtins.input', lambda _: next(expected_inputs))

        expected = True

        actual = gui.confirm(sample_question)
        assert expected == actual

    def test_wait_input_expected_key(self, gui, monkeypatch):
        sample_message = "sample message"
        sample_expected_key = "q"
        expected_input = "q"
        monkeypatch.setattr('builtins.input', lambda _: expected_input)

        gui.wait_input(sample_message, sample_expected_key)
        assert True

    def test_wait_input_not_valid_keys(self, gui, monkeypatch):
        sample_message = "sample message"
        sample_expected_key = "q"
        expected_inputs = iter(["exit", "addaf", "m", "quit", "Q", "q"])
        monkeypatch.setattr('builtins.input', lambda _: next(expected_inputs))

        gui.wait_input(sample_message, sample_expected_key)
        assert True

    def test_get_list_exit_key(self, gui, monkeypatch):
        sample_message = "sample message"
        expected_input = "q"
        monkeypatch.setattr('builtins.input', lambda _: expected_input)

        actual = gui.get_list(sample_message)
        assert len(actual) == 0

    def test_get_list_valid_list(self, gui, options_list, monkeypatch):
        sample_message = "sample message"
        expected_inputs = iter(options_list + ["q"])
        monkeypatch.setattr('builtins.input', lambda _: next(expected_inputs))

        actual = gui.get_list(sample_message)
        assert options_list == actual

    def test_get_list_repeated_item(self, gui, monkeypatch):
        sample_message = "sample message"
        expected_inputs = iter(["option1", "option2", "option2", "q"])
        monkeypatch.setattr('builtins.input', lambda _: next(expected_inputs))

        expected = ["option1", "option2"]

        actual = gui.get_list(sample_message)
        assert expected == actual
