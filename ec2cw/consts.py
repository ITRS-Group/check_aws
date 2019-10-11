from enum import Enum

NAME = "EC2CW"
STATISTICS = ["Average", "Sum", "SampleCount", "Maximum", "Minimum"]
UNITS = [
    "Percent", "Count",
    "Seconds", "Microseconds", "Milliseconds",
    "Bytes", "Kilobytes", "Megabytes", "Gigabytes", "Terabytes",
    "Bits", "Kilobits", "Megabits", "Gigabits", "Terabits",
    "Bytes/Second", "Kilobytes/Second", "Megabytes/Second", "Gigabytes/Second", "Terabytes/Second",
    "Bits/Second", "Kilobits/Second", "Megabits/Second", "Gigabits/Second", "Terabits/Second", "Count/Second"
]


class Default(Enum):
    namespace = None
    metric = None
    dimensions = None
    unit = None
    profile = "default"
    statistic = "Average"
    period = 60
    lag = 0
    warning = 0
    critical = 0
    verbosity = 0
    delta = 0
