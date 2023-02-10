import abc
import pathlib
import typing


class FileReaderMeta(type, abc.ABC):
    @property
    @abc.abstractmethod
    def supported_file_types(cls):
        raise NotImplementedError()


class FileReader(metaclass=FileReaderMeta):
    def __init__(self, file: pathlib.Path):
        self.file = file

    def __init_subclass__(cls, **kwargs):
        from password_rotator.reader.factory import FileReaderFactory
        FileReaderFactory.register(cls)

    def read(self):
        with self.file.open() as file:
            yield from self._read(file=file)

    @abc.abstractmethod
    def _read(self, file: typing.TextIO) -> typing.Generator[dict, None, None]:
        raise NotImplementedError()
