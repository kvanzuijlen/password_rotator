import collections.abc
import typing

from ..util.factory import BaseFactory

if typing.TYPE_CHECKING:
    from ._base import FileReader


class FileReaderFactory(BaseFactory):
    __registered_readers: dict[str, type["FileReader"]] = {}

    @classmethod
    def register(cls, klass: type["FileReader"]):
        supported_file_types = klass.supported_file_types
        if isinstance(supported_file_types, collections.abc.Iterable) and not isinstance(supported_file_types, str):
            cls.__registered_readers.update({supported_file_type: klass for supported_file_type in supported_file_types})
        else:
            cls.__registered_readers[klass.supported_file_types] = klass

    @classmethod
    def get_file_reader_by_file_type(cls, file_type: str) -> type["FileReader"]:
        return cls.__registered_readers[file_type]
