#!/usr/bin/env python3

import sys

from nagiosplugin import guarded, Check, ScalarContext
from ec2cw import parse_cmdline, CloudWatchResource, CloudWatchSummary


def produce_target(cfg):
    return (
        CloudWatchResource(cfg),
        CloudWatchSummary(
            namespace=cfg.namespace,
            metric=cfg.metric,
            dimensions=cfg.dimensions
        )
    )


@guarded(verbose=False)
def main():
    args = parse_cmdline(sys.argv[1:])

    Check(
        *produce_target(args),
        ScalarContext(args.metric, args.warning, args.critical),
    ).main(verbose=args.verbosity > 0)


if __name__ == "__main__":
    main()
