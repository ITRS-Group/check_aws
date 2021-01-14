from dataclasses import dataclass

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


@dataclass
class InputDefault:
    namespace: str = None
    metric: str = None
    dimensions: tuple = ()
    unit: str = None
    region: str = None
    credentials_file: str = None
    profile: str = "default"
    statistic: str = "Average"
    period: int = 60
    lag: int = 0
    warning: int = 0
    critical: int = 0
    verbosity: int = 0
    delta: int = 0
