import sys

from datetime import datetime, timedelta

import nagiosplugin

from boto import ec2
from cloudwatch.cli import parse_cmdline


class CloudWatch:
    class TimeFrame:
        now = datetime.utcnow()

        def __init__(self, period, lag, delta):
            self.start = self.now - timedelta(seconds=period + lag)
            self.end = self.now - timedelta(seconds=delta)

    def __init__(self, config):
        self.region_name = config.region
        self.profile_name = config.profile

        self.frame = CloudWatch.TimeFrame(config.period, config.lag, config.delta)

        if not ec2.get_region(self.region_name):
            raise nagiosplugin.CheckError("Region {} is unknown".format(self.region_name))

        self.connection = ec2.connect_to_region(self.region_name, profile_name=self.profile_name)

    def get_stats(self):
        self.connection.get_metric_statistics()


@nagiosplugin.guarded(verbose=False)
def main():
    test = CloudWatch(config=parse_cmdline(sys.argv[1:]))


if __name__ == "__main__":
    main()
