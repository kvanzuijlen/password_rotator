from ._base import PasswordManagerParser, PasswordManagerParserMeta
from ..model.secret import SecretEntry


class BitwardenParserMeta(type(PasswordManagerParser)):
    @property
    def password_manager(cls):
        return "bitwarden"


class BitwardenParser(PasswordManagerParser, metaclass=BitwardenParserMeta):
    @staticmethod
    def _filter(password_dict: dict) -> bool:
        is_password = password_dict["type"] == "login"
        if not is_password:
            print(f"skipping entry with {password_dict['type']=}")
        return is_password

    def _parse(self, password_dict: dict) -> SecretEntry:
        return SecretEntry(
            name=password_dict["name"],
            base_uri=self._get_domain(uri=password_dict["login_uri"]),
            uri=password_dict["login_uri"],
            username=password_dict["login_username"],
            secret=password_dict["login_password"],
            totp=password_dict["login_totp"],
        )
