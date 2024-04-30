import logging


__all__ = []


class BookingFormatter(logging.Formatter):

    green = '\x1b[32;20m'
    yellow = '\x1b[33;20m'
    red = '\x1b[31;20m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'
    levelname_format = '%(levelname)s'
    format_str = ':     [%(asctime)s] [%(name)s] %(message)s'
    date_format = '%d-%m-%Y %H:%M:%S'

    COLORS = {
        logging.INFO: green,
        logging.WARNING: yellow,
        logging.ERROR: red,
        logging.CRITICAL: bold_red
    }

    def colorise(self, levelno: int):
        color = self.COLORS.get(levelno)
        return (f'{color}{self.levelname_format}{self.reset}' +
                f'{self.format_str}')

    def format(self, record):
        fmt = self.colorise(record.levelno)
        formatter = logging.Formatter(fmt=fmt, datefmt=self.date_format)
        return formatter.format(record)


logger = logging.getLogger()
