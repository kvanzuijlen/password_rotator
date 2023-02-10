import csv
import typing

from ._base import FileReader


class CSVReaderMeta(type(FileReader)):
    @property
    def supported_file_types(cls) -> str | tuple[str, ...]:
        return "csv", "tsv"


class CSVReader(FileReader, metaclass=CSVReaderMeta):
    def _read(self, file: typing.TextIO) -> typing.Generator[dict, None, None]:
        reader = csv.DictReader(file)
        yield from reader
