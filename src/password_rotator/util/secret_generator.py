import dataclasses
import random
import secrets
import string
import typing
from typing import Callable, Dict

if typing.TYPE_CHECKING:
    from password_rotator.model.secret import Secret


@dataclasses.dataclass
class SecretRequirements:
    min_length: int = 20
    max_length: int = 40


@dataclasses.dataclass
class PassphraseRequirements(SecretRequirements):
    delimiter: str = "-"
    allow_uppercase: bool = True
    min_amount_numbers: int = 0
    max_amount_numbers: int = 0
    min_amount_special_characters: int = 0
    max_amount_special_characters: int = 0


@dataclasses.dataclass
class PasswordRequirements(SecretRequirements):
    min_amount_lowercase: int = 1
    min_amount_uppercase: int = 1
    max_amount_uppercase: int = 5
    min_amount_numbers: int = 1
    max_amount_numbers: int = 5
    min_amount_special_characters: int = 1
    max_amount_special_characters: int = 5
    avoid_ambiguous_characters: bool = True


def generate_secure_passphrase(requirements: PassphraseRequirements) -> "Secret":
    from xkcdpass import xkcd_password
    wordlist = xkcd_password.generate_wordlist()
    case = "lower"
    if requirements.allow_uppercase:
        case = "random"

    amount_numbers = random.randint(requirements.min_amount_numbers, requirements.max_amount_numbers)
    amount_special_characters = random.randint(
        requirements.min_amount_special_characters,
        requirements.max_amount_special_characters,
    )

    password = xkcd_password.generate_xkcdpassword(wordlist=wordlist, delimiter="-", case=case)
    random_numbers = [secrets.choice(string.digits) for _ in range(amount_numbers)]
    random_special_characters = [secrets.choice(string.punctuation) for _ in range(amount_special_characters)]
    return Secret(f"{password}{''.join(random_numbers + random_special_characters)}")


def generate_secure_password(requirements: PasswordRequirements) -> "Secret":
    amount_uppercase = random.randint(requirements.min_amount_uppercase, requirements.max_amount_uppercase)
    amount_numbers = random.randint(requirements.min_amount_numbers, requirements.max_amount_numbers)
    amount_special_characters = random.randint(
        requirements.min_amount_special_characters,
        requirements.max_amount_special_characters,
    )
    total_non_lower_characters = sum((amount_uppercase, amount_numbers, amount_special_characters))
    if sum((total_non_lower_characters, requirements.min_amount_lowercase)) > requirements.max_length:
        return generate_secure_password(requirements=PasswordRequirements(
            min_length=requirements.min_length,
            max_length=requirements.max_length,
            min_amount_lowercase=requirements.min_amount_lowercase,
            min_amount_uppercase=requirements.min_amount_uppercase,
            max_amount_uppercase=amount_uppercase,
            min_amount_numbers=requirements.min_amount_numbers,
            max_amount_numbers=amount_numbers,
            min_amount_special_characters=requirements.min_amount_special_characters,
            max_amount_special_characters=amount_special_characters,
            avoid_ambiguous_characters=requirements.avoid_ambiguous_characters,
        ))
    min_required_lowercase = max(requirements.min_amount_lowercase, requirements.min_length - total_non_lower_characters)
    max_possible_lowercase = max(requirements.min_amount_lowercase, requirements.max_length - total_non_lower_characters)
    amount_lowercase = random.randint(min_required_lowercase, max_possible_lowercase)

    uppercase_letters = [secrets.choice(string.ascii_uppercase) for _ in range(amount_uppercase)]
    numbers = [secrets.choice(string.digits) for _ in range(amount_numbers)]
    special_characters = [secrets.choice(string.punctuation) for _ in range(amount_special_characters)]
    lowercase_letters = [secrets.choice(string.ascii_lowercase) for _ in range(amount_lowercase)]

    password_characters = uppercase_letters + numbers + special_characters + lowercase_letters
    random.shuffle(password_characters)

    return Secret("".join(password_characters))


def supported_generators() -> dict[str, Callable[[PassphraseRequirements], "Secret"] | Callable[[PasswordRequirements], "Secret"]]:
    return {
        "passphrase": generate_secure_passphrase,
        "secret": generate_secure_password,
    }
