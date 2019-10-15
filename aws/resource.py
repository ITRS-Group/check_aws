import os

from collections import namedtuple
from datetime import datetime, timedelta

import nagiosplugin

from boto.ec2 import cloudwatch
from boto.provider import Provider
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

    def probe(self):
        def get_config(keys):
            return {k: config.get(self.cfg.profile, k) for k in keys}

        config = Config(do_load=False)
        config.load_from_path(
            self.cfg.credentials_file or get_default_credentials_file()
        )
        connection = cloudwatch.connect_to_region(
            self.cfg.region,
            **get_config(["aws_access_key_id", "aws_secret_access_key"])
        )

        points = connection.get_metric_statistics(**self.payload)

        if len(points) < 1:
            return []

        point = points[0]
        return [nagiosplugin.Metric(self.cfg.metric, point[self.cfg.statistic])]

    @property
    def name(self):
        return NAME
