import argparse

from os import path
from pathlib import Path

from .options import opts
from aws.consts import UNITS


def get_default_credentials_file():
    homedir = path.expanduser("~")
    return path.join(homedir, ".aws", "credentials")


def parse_cmdline(args):
    parser = argparse.ArgumentParser(
        description="Plugin for monitoring CloudWatch-enabled AWS instances"
    )

    for opt, conf in opts:
        parser.add_argument(*opt, **conf)

    parsed = parser.parse_args(args)

    if parsed.unit and parsed.unit not in UNITS:
        raise ValueError("Unit must be one of: {}".format(UNITS))

    cf = parsed.credentials_file

    if not cf:
        parsed.credentials_file = get_default_credentials_file()
    elif not Path(cf).exists():
        raise OSError("File {} does not exist".format(cf))

    return parsed
