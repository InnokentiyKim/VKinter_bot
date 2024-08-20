import logging
from functools import wraps
from logging.handlers import RotatingFileHandler


LOGGER_PATH = 'bot_logging/bot.log'


error_logger = logging.getLogger(LOGGER_PATH)
error_logger.setLevel(logging.ERROR)
error_handler = RotatingFileHandler(LOGGER_PATH, maxBytes=10000000, backupCount=5)
error_formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s',
                              datefmt='%d-%m-%Y %H:%M:%S')
error_handler.setFormatter(error_formatter)
error_logger.addHandler(error_handler)


def bot_exception_logger(path: str, exc_info: bool = False):
    __logger = logging.getLogger(path)
    __logger.setLevel(logging.ERROR)
    handler = RotatingFileHandler(path, maxBytes=10000000, backupCount=5)
    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s',
                                  datefmt='%d-%m-%Y %H:%M:%S')
    handler.setFormatter(formatter)
    __logger.addHandler(handler)
    def _logger(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as error:
                __logger.error(f'Вызов функции {function.__name__} с параметрами {args}, {kwargs} вызвал ошибку {error}',
                               exc_info=exc_info)
        return wrapper
    return _logger
