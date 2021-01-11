from os import path

from enum import Enum

NAME = "AWS"
STATISTICS = ["Average", "Sum", "SampleCount", "Maximum", "Minimum"]
UNITS = [
    "Percent",
    "Count",
    "Seconds",
    "Microseconds",
    "Milliseconds",
    "Bytes",
    "Kilobytes",
    "Megabytes",
    "Gigabytes",
    "Terabytes",
    "Bits",
    "Kilobits",
    "Megabits",
    "Gigabits",
    "Terabits",
    "Bytes/Second",
    "Kilobytes/Second",
    "Megabytes/Second",
    "Gigabytes/Second",
    "Terabytes/Second",
    "Bits/Second",
    "Kilobits/Second",
    "Megabits/Second",
    "Gigabits/Second",
    "Terabits/Second",
    "Count/Second",
]


class Default(Enum):
    namespace = None
    metric = None
    dimensions = ()
    unit = "Count"
    credentials_file = path.join(path.expanduser("~"), ".aws", "credentials")
    profile = "default"
    statistic = "Average"
    period = 60
    lag = 0
    warning = 0
    critical = 0
    verbosity = 0
    delta = 0
