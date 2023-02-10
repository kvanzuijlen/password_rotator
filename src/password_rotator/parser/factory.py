import typing

from ..util.factory import BaseFactory

if typing.TYPE_CHECKING:
    from ._base import PasswordManagerParser


class PasswordManagerParserFactory(BaseFactory):
    __registered_readers: dict[str, type["PasswordManagerParser"]] = {}

    @classmethod
    def register(cls, klass: type["PasswordManagerParser"]):
        cls.__registered_readers[klass.password_manager] = klass

    @classmethod
    def get_supported_password_managers(cls) -> tuple:
        return tuple(cls.__registered_readers.keys())

    @classmethod
    def get_password_manager_parser(cls, password_manager: str) -> type["PasswordManagerParser"]:
        return cls.__registered_readers[password_manager]
