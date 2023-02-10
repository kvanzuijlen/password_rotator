import dataclasses
import typing


class Secret(str):
    def __repr__(self):
        return f"{self[0]}***{self[-1]}"


@dataclasses.dataclass
class SecretEntry:
    name: typing.Optional[str]
    base_uri: str
    uri: str
    username: str
    secret: Secret
    totp: str

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"SecretEntry({self.name=}, {self.base_uri=}, {self.uri=}, {self.username=}, {self.secret=}, {self.totp=})"
