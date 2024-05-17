import logging
from habit_tracker import settings


def config_logger():
    logging.basicConfig(
        filename=settings.LOGS_DIR / 'output.log',
        level=logging.DEBUG
    )
