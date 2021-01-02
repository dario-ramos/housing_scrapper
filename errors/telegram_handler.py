from .abstract_handler import AbstractErrorHandler
import traceback
import html


class TelegramErrorHandler(AbstractErrorHandler):

    def __init__(self, notifier):
        self.notifier = notifier

    def handle_exception(self, msg: str, e: Exception):
        e_str = html.escape(
            ''.join(traceback.format_exception(None, e, e.__traceback__)))
        self.notifier.notify_error(
            msg + '. Detailed error information: ' + e_str)
