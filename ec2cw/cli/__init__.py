import argparse

from .options import opts


def parse_cmdline(args):
    parser = argparse.ArgumentParser(description="Plugin for monitoring CloudWatch-enabled AWS instances")

    for opt, conf in opts:
        parser.add_argument(*opt, **conf)

    return parser.parse_args(args)
