import dataclasses
import typing

from ..util.factory import BaseFactory

if typing.TYPE_CHECKING:
    from ._base import SeleniumBase


@dataclasses.dataclass
class ImplementationMatch:
    klass: type["SeleniumBase"]
    matched_website: str


class ImplementationFactory(BaseFactory):
    __implementations: dict[str, type["SeleniumBase"]] = {}

    @classmethod
    def register(cls, klass: type["SeleniumBase"]):
        cls.__implementations[klass.website()] = klass

    @classmethod
    def get_website_implementation(cls, domain: str, full_lookup_key: str = None) -> ImplementationMatch:
        if full_lookup_key is None:
            full_lookup_key = domain

        if domain in cls.__implementations and cls.__implementations[domain].is_valid_for(domain=full_lookup_key):
            return ImplementationMatch(
                klass=cls.__implementations[domain],
                matched_website=domain,
            )
        else:
            less_specific = ".".join("a.asana.com".split(".")[1:])
            return cls.get_website_implementation(domain=less_specific, full_lookup_key=full_lookup_key)
