from boto3 import Session

from nagios_aws.consts import STATISTICS, InputDefault

from .actions import CredentialsFileParser, DimensionsSerializer

opts = [
    (
        ["-r", "--region"],
        {
            "dest": "region",
            "action": "store",
            "type": str,
            "default": InputDefault.metric,
            "choices": Session().get_available_regions("ec2"),
            "required": True,
            "help": "AWS region name",
        },
    ),
    (
        ["-u", "--unit"],
        {
            "dest": "unit",
            "action": "store",
            "type": str,
            "default": InputDefault.unit,
            "required": True,
            "help": "Response unit",
        },
    ),
    (
        ["-m", "--metric"],
        {
            "dest": "metric",
            "action": "store",
            "type": str,
            "default": InputDefault.metric,
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
            "default": InputDefault.namespace,
            "required": True,
            "help": "Metric namespace",
        },
    ),
    (
        ["-d", "--dimensions"],
        {
            "dest": "dimensions",
            "action": DimensionsSerializer,
            "type": str,
            "nargs": "?",
            "default": InputDefault.dimensions,
            "help": "Dimensions of one or more metrics: dimension=value[,dimension=value...]",
        },
    ),
    (
        ["-p", "--profile"],
        {
            "dest": "profile",
            "action": "store",
            "type": str,
            "default": InputDefault.profile,
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
            "default": InputDefault.statistic,
            "help": "Statistic for evaluating metrics (default: %(default)s)",
        },
    ),
    (
        ["-w", "--warning"],
        {
            "dest": "warning",
            "action": "store",
            "type": str,
            "default": InputDefault.warning,
            "help": "Warning if threshold is outside range (default: %(default)s)",
        },
    ),
    (
        ["-c", "--critical"],
        {
            "dest": "critical",
            "action": "store",
            "type": str,
            "default": InputDefault.critical,
            "help": "Critical if threshold is outside range (default: %(default)s)",
        },
    ),
    (
        ["-v", "--verbosity"],
        {
            "dest": "verbosity",
            "action": "count",
            "default": InputDefault.verbosity,
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
            "default": InputDefault.period,
            "help": "Period in seconds over which the statistic is applied (default: %(default)s)",
        },
    ),
    (
        ["-D", "--delta"],
        {
            "dest": "delta",
            "action": "store",
            "type": int,
            "default": InputDefault.delta,
            "help": "Delta measurement in seconds",
        },
    ),
    (
        ["-l", "--lag"],
        {
            "dest": "lag",
            "action": "store",
            "type": int,
            "default": InputDefault.lag,
            "help": "Delay in seconds to add to starting time for gathering metric."
            "useful for ec2 basic monitoring which aggregates over 5min periods (default: %(default)s)",
        },
    ),
    (
        ["-C", "--credentials"],
        {
            "dest": "credentials_file",
            "action": CredentialsFileParser,
            "type": str,
            "nargs": "?",
            "default": InputDefault.credentials_file,
            "help": "File containing AWS credentials (DEPRECATED)",
        },
    ),
    (
        ["-f", "--credentials_file"],
        {
            "dest": "credentials_file",
            "action": CredentialsFileParser,
            "type": str,
            "nargs": "?",
            "default": InputDefault.credentials_file,
            "help": "File containing AWS credentials",
        },
    ),
]
