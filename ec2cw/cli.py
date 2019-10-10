import argparse

from enum import Enum

from boto import ec2

from .consts import STATISTICS


class DimensionParser(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        kvs = {}
        for pair in values.split(','):
            k, v = pair.split('=')
            kvs[k] = v

        setattr(namespace, self.dest, kvs)


class Default(Enum):
    namespace = None
    metric = None
    dimensions = None
    profile = "default"
    statistic = "Average"
    period = 60
    lag = 0
    warning = 0
    critical = 0
    verbosity = 0
    delta = 0


opts = [
    (
        ["-r", "--region"],
        {
            "dest": "region",
            "action": "store",
            "type": str,
            "default": Default.metric.value,
            "choices": [region.name for region in ec2.get_regions("ec2")],
            "required": True,
            "help": "CloudWatch metric name"
        }
    ),
    (
        ["-m", "--metric"],
        {
            "dest": "metric",
            "action": "store",
            "type": str,
            "default": Default.metric.value,
            "required": True,
            "help": "CloudWatch metric name"
        }
    ),
    (
        ["-n", "--namespace"],
        {
            "dest": "namespace",
            "action": "store",
            "type": str,
            "default": Default.namespace.value,
            "required": True,
            "help": "CloudWatch metric namespace"
        }
    ),
    (
        ["-d", "--dimensions"],
        {
            "dest": "dimensions",
            "action": DimensionParser,
            "type": str,
            "default": Default.dimensions.value,
            "help": "Dimensions of one or more metrics: dimension=value[,dimension=value...]"
        }
    ),
    (
        ["-p", "--profile"],
        {
            "dest": "profile",
            "action": "store",
            "type": str,
            "default": Default.profile.value,
            "help": "Profile name from ~/.aws/credentials (default: %(default)s)"
        }
    ),
    (
        ["-s", "--statistic"],
        {
            "dest": "statistic",
            "action": "store",
            "type": str,
            "choices": STATISTICS,
            "default": Default.statistic.value,
            "help": "Statistic for evaluating metrics (default: %(default)s)"
        }
    ),
    (
        ["-w", "--warning"],
        {
            "dest": "warning",
            "action": "store",
            "default": Default.warning.value,
            "help": "Warning if threshold is outside range (default: %(default)s)"
        }
    ),
    (
        ["-c", "--critical"],
        {
            "dest": "critical",
            "action": "store",
            "default": Default.critical.value,
            "help": "Critical if threshold is outside range (default: %(default)s)"
        }
    ),
    (
        ["-v", "--verbosity"],
        {
            "dest": "verbosity",
            "action": "count",
            "default": Default.verbosity.value,
            "help": "Set verbosity (use up to 3 times)"
        }
    ),
    (
        ["-P", "--period"],
        {
            "dest": "period",
            "action": "store",
            "type": int,
            "default": Default.period.value,
            "help": "Period in seconds over which the statistic is applied (default: %(default)s)"
        }
    ),
    (
        ["-D", "--delta"],
        {
            "dest": "delta",
            "action": "store",
            "type": int,
            "default": Default.delta.value,
            "help": "Delta measurement in seconds"
        }
    ),
    (
        ["-l", "--lag"],
        {
            "dest": "lag",
            "action": "store",
            "type": int,
            "default": Default.lag.value,
            "help": "Delay in seconds to add to starting time for gathering metric."
                    "useful for ec2 basic monitoring which aggregates over 5min periods (default: %(default)s)",
        }
    ),
]


def parse_cmdline(args):
    parser = argparse.ArgumentParser(description="Plugin for monitoring CloudWatch-enabled AWS instances")

    for opt, conf in opts:
        parser.add_argument(*opt, **conf)

    return parser.parse_args(args)
