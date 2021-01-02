import abc


class AbstractErrorHandler(abc.ABC):

    @abc.abstractmethod
    def handle_exception(self, msg: str, e: Exception):
        raise NotImplementedError
