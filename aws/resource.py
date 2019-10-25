import os

from collections import namedtuple
from datetime import datetime, timedelta

import nagiosplugin

from boto.ec2 import cloudwatch
from boto.pyami.config import Config

from .consts import NAME

TimeFrame = namedtuple("TimeFrame", ["start", "end"])


class CloudWatchResource(nagiosplugin.Resource):
    def __init__(self, cfg):
        self.cfg = cfg

        now = datetime.utcnow()

        self.frame = TimeFrame(
            start=now - timedelta(seconds=cfg.period + cfg.lag),
            end=now - timedelta(seconds=cfg.delta),
        )

        self.payload = dict(
            period=self.cfg.period,
            start_time=self.frame.start,
            end_time=self.frame.end,
            metric_name=self.cfg.metric,
            namespace=self.cfg.namespace,
            statistics=self.cfg.statistic,
            dimensions=self.cfg.dimensions,
            unit=self.cfg.unit,
        )

    def get_config(self, keys=None):
        keys = keys or ["aws_access_key_id", "aws_secret_access_key"]
        config = Config(do_load=False)
        config.load_from_path(self.cfg.credentials_file)

        return {k: config.get(self.cfg.profile, k) for k in keys}

    @property
    def connection(self):
        return cloudwatch.connect_to_region(
            self.cfg.region,
            **self.get_config()
        )

    def _request(self):
        return self.connection.get_metric_statistics(**self.payload)

    def probe(self):
        points = self._request()

        if len(points) < 1:
            return []

        point = points[0]

        return [nagiosplugin.Metric(self.cfg.metric, point[self.cfg.statistic])]

    @property
    def name(self):
        return NAME
