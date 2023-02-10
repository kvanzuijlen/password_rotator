import pathlib

import click

from password_rotator.parser.factory import PasswordManagerParserFactory
from password_rotator.rotate import PasswordRotator
from password_rotator.util.secret_generator import supported_generators


@click.command()
@click.option("--password_manager", "--pm",
              type=click.Choice(PasswordManagerParserFactory.get_supported_password_managers(), case_sensitive=False),
              required=True)
@click.option("--file", type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path), required=True)
@click.option("--preferred_generator", type=click.Choice(tuple(supported_generators().keys())), default="passphrase")
def cli(password_manager: str, file: pathlib.Path, preferred_generator: str):
    PasswordRotator(password_manager=password_manager, file=file, preferred_generator=preferred_generator).rotate()
