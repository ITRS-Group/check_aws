from collections import namedtuple
from datetime import datetime, timedelta

import nagiosplugin

from boto.ec2 import cloudwatch

from .consts import NAME

TimeFrame = namedtuple("TimeFrame", ["start", "end"])


class CloudWatchResource(nagiosplugin.Resource):
    def __init__(self, cfg):
        self.cfg = cfg

        now = datetime.utcnow()
        self.frame = TimeFrame(
            start=now - timedelta(seconds=cfg.period + cfg.lag),
            end=now - timedelta(seconds=cfg.delta)
        )

    @property
    def payload(self):
        return dict(
            period=self.cfg.period,
            start_time=self.frame.start,
            end_time=self.frame.end,
            metric_name=self.cfg.metric,
            namespace=self.cfg.namespace,
            statistics=self.cfg.statistic,
            dimensions=self.cfg.dimensions,
        )

    def probe(self):
        connection = cloudwatch.connect_to_region(
            self.cfg.region, profile_name=self.cfg.profile
        )

        points = connection.get_metric_statistics(**self.payload)

        if len(points) < 1:
            return []

        point = points[0]
        return [nagiosplugin.Metric(self.cfg.metric, point[self.cfg.statistic])]

    @property
    def name(self):
        return NAME
