from collections import namedtuple
from datetime import datetime, timedelta

import boto3
import nagiosplugin

from .consts import NAME
from .exceptions import UnexpectedResponse

TimeFrame = namedtuple("TimeFrame", ["start", "end"])


class CloudWatchResource(nagiosplugin.Resource):
    def __init__(self, cfg, *args, **kwargs):
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

        self._session = boto3.Session(region_name=self.cfg.region)

        super(CloudWatchResource, self).__init__(*args, **kwargs)

    @property
    def connection(self):
        return self._session.client("cloudwatch")

    def _send(self, *args, **kwargs):
        return self.connection.get_metric_statistics(*args, **self.payload, **kwargs)

    def probe(self):
        """Generator for yielding metrics from Datapoints"""

        response = self._send()
        if "Datapoints" not in response or len(response["Datapoints"]) < 1:
            return []

        # Make statistic input case insensitive
        stat_key = self.cfg.statistic.capitalize()
        label = response["Label"]

        if label != self.cfg.metric:
            raise UnexpectedResponse(
                f"Unexpected Metric in Response. Got: {label}, Expected: {self.cfg.metric}"
            )

        for point in response["Datapoints"]:
            stat_val = point.get(stat_key)

            yield nagiosplugin.Metric(self.cfg.metric, stat_val)

    @property
    def name(self):
        return NAME
