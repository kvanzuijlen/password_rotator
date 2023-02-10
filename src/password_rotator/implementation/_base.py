import abc
import typing

from selenium import webdriver

if typing.TYPE_CHECKING:
    from password_rotator.model.secret import Secret, SecretEntry
    from password_rotator.util.secret_generator import PasswordRequirements, PassphraseRequirements


class SeleniumBase(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def passphrase_requirements(cls) -> "PassphraseRequirements":
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def password_requirements(cls) -> "PasswordRequirements":
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def website(cls) -> str:
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def is_valid_for(cls, domain: str) -> bool:
        raise NotImplementedError()

    def __init__(self, password_entry: "SecretEntry", new_password: "Secret"):
        self.driver = None
        self._password_entry = password_entry
        self._new_password = new_password

    def __enter__(self):
        self.driver = webdriver.Firefox()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def run(self):
        if self.driver is None:
            raise RuntimeError()
        self._change_password()

    @abc.abstractmethod
    def _change_password(self):
        raise NotImplementedError()
