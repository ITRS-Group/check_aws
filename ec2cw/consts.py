from enum import Enum

NAME = "EC2CW"
STATISTICS = ["Average", "Sum", "SampleCount", "Maximum", "Minimum"]


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
