from .stdout_handler import StdOutErrorHandler
from .telegram_handler import TelegramErrorHandler


def create_error_handler(name, notifier):
    if name == 'stdout':
        return StdOutErrorHandler()
    elif name == 'telegram':
        return TelegramErrorHandler(notifier)
    else:
        raise LookupError(
            f"Invalid error handler {name}. Supported values: stdout, telegram")
