import abc
from .model import Property


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, prop: Property):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, prop) -> Property:
        raise NotImplementedError
