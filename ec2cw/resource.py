from collections import namedtuple
from datetime import datetime, timedelta

import nagiosplugin

from boto.ec2 import cloudwatch

from .consts import NAME

TimeFrame = namedtuple("TimeFrame", ["start", "end"])


class CloudWatchResource(nagiosplugin.Resource):
    def __init__(self, cfg):
        self._cfg = cfg

        now = datetime.utcnow()
        self.frame = TimeFrame(
            start=now - timedelta(seconds=cfg.period + cfg.lag),
            end=now - timedelta(seconds=cfg.delta)
        )

        self.connection = cloudwatch.connect_to_region(
            cfg.region, profile_name=cfg.profile
        )

    def probe(self):
        points = self.connection.get_metric_statistics(
            period=self._cfg.period,
            start_time=self.frame.start,
            end_time=self.frame.end,
            metric_name=self._cfg.metric,
            namespace=self._cfg.namespace,
            statistics=self._cfg.statistic,
            dimensions=self._cfg.dimensions,
        )

        if len(points) < 1:
            return []

        point = points[0]
        return [nagiosplugin.Metric(self._cfg.metric, point[self._cfg.statistic])]

    @property
    def name(self):
        return NAME
