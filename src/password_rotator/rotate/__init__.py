import pathlib
import typing

from password_rotator.parser import PasswordManagerParserFactory
from password_rotator.reader.factory import FileReaderFactory
from password_rotator.util.secret_generator import supported_generators

if typing.TYPE_CHECKING:
    from password_rotator.implementation import SeleniumBase


class PasswordRotator:
    def __init__(self, password_manager: str, preferred_generator: str, file: pathlib.Path, file_type: str = None):
        self.password_manager = password_manager
        self.preferred_generator = supported_generators()[preferred_generator]
        self._preferred_generator = preferred_generator
        self.file = file
        self.file_type = file_type
        if file_type is None:
            self.file_type = file.suffix.lstrip(".")

        reader = FileReaderFactory.get_file_reader_by_file_type(file_type=self.file_type)(file=file)
        parser_cls = PasswordManagerParserFactory.get_password_manager_parser(password_manager=password_manager)

        self._password_manager_parser = parser_cls(reader=reader)

    def rotate(self):
        for password in self._password_manager_parser.parse():
            selenium_impl = self._get_selenium_impl(domain=password.base_uri)
            if selenium_impl is None:
                print(f"No implementation exists for {password.base_uri=} trying the fallback implementation")
                continue
            print(f"Changing secret for {password.base_uri=}")
            requirements = selenium_impl.passphrase_requirements()
            if self._preferred_generator == "secret":
                requirements = selenium_impl.password_requirements()

            print(f"Generating {self._preferred_generator} for {password.base_uri=} with {requirements=}")
            new_password = self.preferred_generator(requirements)

            selenium_impl(password_entry=password, new_password=new_password).run()

    @staticmethod
    def _get_selenium_impl(domain: str) -> type["SeleniumBase"]:
        from password_rotator.implementation.factory import ImplementationFactory
        if implementation := ImplementationFactory.get_website_implementation(domain=domain):
            return implementation.klass
