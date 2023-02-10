import abc


class BaseFactory(abc.ABC):
    @classmethod
    def register(cls, klass: type):
        raise NotImplementedError()
