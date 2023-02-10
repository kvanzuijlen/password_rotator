import abc
import typing
import urllib.parse

from password_rotator.model.secret import SecretEntry

if typing.TYPE_CHECKING:
    from password_rotator.reader._base import FileReader


class PasswordManagerParserMeta(type, abc.ABC):
    @property
    @abc.abstractmethod
    def password_manager(cls):
        raise NotImplementedError()


class PasswordManagerParser(metaclass=PasswordManagerParserMeta):
    def __init__(self, reader: "FileReader"):
        self.reader = reader

    def __init_subclass__(cls, **kwargs):
        from .factory import PasswordManagerParserFactory
        PasswordManagerParserFactory.register(klass=cls)

    def parse(self) -> typing.Generator[SecretEntry, None, None]:
        for password_dict in self.reader.read():
            if self._filter(password_dict=password_dict):
                yield self._parse(password_dict=password_dict)

    @abc.abstractmethod
    def _parse(self, password_dict: dict) -> SecretEntry:
        raise NotImplementedError()

    @staticmethod
    def _filter(password_dict: dict) -> bool:
        return True

    def _get_domain(self, uri: str) -> str:
        return urllib.parse.urlparse(url=uri).netloc
