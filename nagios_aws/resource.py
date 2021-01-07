from collections import namedtuple
from datetime import datetime, timedelta

import nagiosplugin
import boto3

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
            Period=self.cfg.period,
            StartTime=self.frame.start,
            EndTime=self.frame.end,
            MetricName=self.cfg.metric,
            Namespace=self.cfg.namespace,
            Statistics=(self.cfg.statistic,),
            Dimensions=self.cfg.dimensions,
            Unit=self.cfg.unit,
        )

    @property
    def connection(self):
        session = boto3.Session(region_name=self.cfg.region)
        return session.client("cloudwatch")

    def _send(self, *args, **kwargs):
        return self.connection.get_metric_statistics(*args, **self.payload, **kwargs)

    def probe(self):
        """Generator for yielding metrics from Datapoints"""

        response = self._send()
        if len(response["Datapoints"]) < 1:
            return []

        # Make stat key case insensitive
        stat_key = self.cfg.statistic.capitalize()

        for point in response["Datapoints"]:
            stat_val = point.get(stat_key)
            yield nagiosplugin.Metric(self.cfg.metric, stat_val)

    @property
    def name(self):
        return NAME
