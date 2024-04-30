import logging
from logger import BookingFormatter, logger
from settings import get_settings


def configure():
    '''
    Configures app.
    '''
    _configure_logger()
    get_settings()


def _configure_logger():
    sh = logging.StreamHandler()

    sh.setLevel(logging.INFO)
    sh.set_name("booking")
    sh.setFormatter(BookingFormatter())

    logger.name = "booking"
    logger.addHandler(sh)
    logger.setLevel(logging.INFO)
