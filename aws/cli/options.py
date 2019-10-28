from boto import ec2

from aws.consts import STATISTICS, Default

from .parsers import DimensionParser

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
            "help": "AWS region name"
        }
    ),
    (
        ["-u", "--unit"],
        {
            "dest": "unit",
            "action": "store",
            "type": str,
            "default": Default.unit.value,
            "required": False,
            "help": "Metric Unit"
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
            "nargs": "?",
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
            "type": str,
            "default": Default.warning.value,
            "help": "Warning if threshold is outside range (default: %(default)s)"
        }
    ),
    (
        ["-c", "--critical"],
        {
            "dest": "critical",
            "action": "store",
            "type": str,
            "default": Default.critical.value,
            "help": "Critical if threshold is outside range (default: %(default)s)"
        }
    ),
    (
        ["-v", "--verbosity"],
        {
            "dest": "verbosity",
            "action": "count",
            "type": str,
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
            "nargs": "?",
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
    (
        ["-C", "--credentials"],
        {
            "dest": "credentials_file",
            "action": "store",
            "type": str,
            "nargs": "?",
            "default": Default.credentials_file.value,
            "help": "File containing AWS credentials"
        }
    ),
]
