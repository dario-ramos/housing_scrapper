import logging
import traceback

from .abstract_handler import AbstractErrorHandler


class StdOutErrorHandler(AbstractErrorHandler):

    def handle_exception(self, msg: str, e: Exception):
        logging.error(msg)
        logging.error(
            ''.join(traceback.format_exception(None, e, e.__traceback__)))
