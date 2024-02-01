from dataclasses import dataclass

from boto3 import Session

from ..consts import STATISTICS
from .actions import CredentialsFileSetter, DimensionsSerializer


@dataclass
class CommandArguments:
    namespace: str = ""
    metric: str = ""
    unit: str = ""
    region: str = ""
    credentials_file: str = ""
    profile: str = "default"
    statistic: str = "Average"
    dimensions: tuple = ()
    period: int = 60
    lag: int = 0
    warning: int = 0
    critical: int = 0
    verbosity: int = 0
    delta: int = 0
    timeout: int = 0


opts = [
    (
        ["-r", "--region"],
        {
            "dest": "region",
            "action": "store",
            "type": str,
            "default": CommandArguments.region,
            "choices": Session().get_available_regions("ec2"),
            "required": True,
            "help": "AWS Region",
        },
    ),
    (
        ["-u", "--unit"],
        {
            "dest": "unit",
            "action": "store",
            "type": str,
            "default": CommandArguments.unit,
            "required": False,
            "help": "Expected unit in the response",
        },
    ),
    (
        ["-m", "--metric"],
        {
            "dest": "metric",
            "action": "store",
            "type": str,
            "default": CommandArguments.metric,
            "required": True,
            "help": "Metric name",
        },
    ),
    (
        ["-n", "--namespace"],
        {
            "dest": "namespace",
            "action": "store",
            "type": str,
            "default": CommandArguments.namespace,
            "required": True,
            "help": "Service Namespace",
        },
    ),
    (
        ["-d", "--dimensions"],
        {
            "dest": "dimensions",
            "action": DimensionsSerializer,
            "type": str,
            "nargs": "?",
            "default": CommandArguments.dimensions,
            "help": "One or more Dimensions for selecting metric data: dimension=value[,dimension=value...]",
        },
    ),
    (
        ["-p", "--profile"],
        {
            "dest": "profile",
            "action": "store",
            "type": str,
            "default": CommandArguments.profile,
            "help": "Profile name from ~/.aws/credentials (default: %(default)s)",
        },
    ),
    (
        ["-s", "--statistic"],
        {
            "dest": "statistic",
            "action": "store",
            "type": str,
            "choices": STATISTICS,
            "default": CommandArguments.statistic,
            "help": "Statistic for evaluating metrics (default: %(default)s)",
        },
    ),
    (
        ["-w", "--warning"],
        {
            "dest": "warning",
            "action": "store",
            "type": str,
            "default": CommandArguments.warning,
            "help": "Warning if threshold is outside range (default: %(default)s)",
        },
    ),
    (
        ["-c", "--critical"],
        {
            "dest": "critical",
            "action": "store",
            "type": str,
            "default": CommandArguments.critical,
            "help": "Critical if threshold is outside range (default: %(default)s)",
        },
    ),
    (
        ["-v", "--verbosity"],
        {
            "dest": "verbosity",
            "action": "count",
            "default": CommandArguments.verbosity,
            "help": "Verbosity (use up to 3 times)",
        },
    ),
    (
        ["-P", "--period"],
        {
            "dest": "period",
            "action": "store",
            "type": int,
            "nargs": "?",
            "default": CommandArguments.period,
            "help": "Period in seconds over which the statistic is applied (default: %(default)s)",
        },
    ),
    (
        ["-D", "--delta"],
        {
            "dest": "delta",
            "action": "store",
            "type": int,
            "default": CommandArguments.delta,
            "help": "Delta measurement in seconds",
        },
    ),
    (
        ["-l", "--lag"],
        {
            "dest": "lag",
            "action": "store",
            "type": int,
            "default": CommandArguments.lag,
            "help": "Delay in seconds to add to starting time (default: %(default)s)",
        },
    ),
    (
        ["-C", "--credentials"],
        {
            "dest": "credentials_file",
            "action": CredentialsFileSetter,
            "type": str,
            "nargs": "?",
            "default": CommandArguments.credentials_file,
            "help": "File containing AWS credentials (DEPRECATED)",
        },
    ),
    (
        ["-f", "--credentials_file"],
        {
            "dest": "credentials_file",
            "action": CredentialsFileSetter,
            "type": str,
            "nargs": "?",
            "default": CommandArguments.credentials_file,
            "help": "File containing AWS credentials",
        },
    ),
    (
        ["-t", "--timeout"],
        {
            "dest": "timeout",
            "action": "store",
            "type": int,
            "default": CommandArguments.timeout,
            "required": False,
            "help": "Timeout in seconds",
        },
    ),
]
