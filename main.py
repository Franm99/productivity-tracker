from habit_tracker.view.cli import CliView
from habit_tracker.controller import Controller
from habit_tracker import config_logger
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    config_logger()

    logger.debug("Initializing program.")

    view = CliView()
    controller = Controller(view)

    controller.run()
