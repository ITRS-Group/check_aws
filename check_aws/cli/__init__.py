import argparse

from check_aws.consts import UNITS

from .options import opts


# @TODO - move to cli.parse
def parse_cmdline(args):
    parser = argparse.ArgumentParser(
        description="Plugin for monitoring CloudWatch-enabled AWS instances"
    )

    for opt, conf in opts:
        parser.add_argument(*opt, **conf)

    parsed = parser.parse_args(args)

    if parsed.unit and parsed.unit not in UNITS:
        raise ValueError("Unit must be one of: {}".format(UNITS))

    return parsed
