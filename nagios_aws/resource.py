from datetime import datetime, timedelta

import boto3
import nagiosplugin

from .consts import NAME
from .exceptions import (
    InvalidDimension,
    InvalidMetricNamespace,
    InvalidMetricType,
    UnexpectedResponse,
)


class CloudWatchResource(nagiosplugin.Resource):
    def __init__(self, cmdargs, *args, **kwargs):
        self.cmdargs = cmdargs
        self.session = boto3.Session(region_name=cmdargs.region)
        super(CloudWatchResource, self).__init__(*args, **kwargs)

    def _query_make(self, cmdargs, validate=True):
        """Transforms cmdargs to a metric statistics query

        Performs validation of Metric + Namespace, and Dimensions if
        validation is set to True.

        Args:
            cmdargs: Argparse object
            validate: Validate query

        Returns:
            Metric statistics query
        """

        now = datetime.utcnow()
        query = dict(
            Period=cmdargs.period,
            StartTime=now - timedelta(seconds=cmdargs.period + cmdargs.lag),
            EndTime=now - timedelta(seconds=cmdargs.delta),
            MetricName=cmdargs.metric,
            Namespace=cmdargs.namespace,
            Statistics=(cmdargs.statistic,),
            Dimensions=cmdargs.dimensions,
            Unit=cmdargs.unit,
        )

        if validate is True:
            self._query_validate(query)

        return query

    def _metrics_get(self, **kwargs):
        """Get a list of available cloudwatch metrics including dimensions

        Args:
            **kwargs: Conditions to pass along to list_metrics()

        Returns:
            Response content
        """

        return self.session.client("cloudwatch").list_metrics(**kwargs)

    def _query_validate(self, query):
        """Validate the given query

        Raises an exception if Metric, Namespace or Dimensions in the query is invalid.

        Raises:
            InvalidDimension: Invalid Dimensions
            InvalidMetricType: Invalid Metric
            InvalidMetricNamespace: No such Metric in Namespace

        Returns:
            True
        """

        namespace, metric = query["Namespace"], query["MetricName"]
        avail_dimensions = []
        # Convert dimensions in query to a set of key-value pairs, for comparison with `dimensions`
        req_dimensions = set(
            [(d["Name"], d["Value"]) for d in query.get("Dimensions", ()) if d]
        )

        response = self._metrics_get(Namespace=namespace, MetricName=metric)

        # Perform validation
        if not response.get("Metrics"):
            # Figure out what went wrong
            response = self._metrics_get(MetricName=metric)
            if response.get("Metrics"):  # Does the given metric exist?
                raise InvalidMetricNamespace(
                    f"No metric of type '{metric}' in Namespace '{namespace}'"
                )
            else:  # Invalid metric type
                raise InvalidMetricType(f"No such metric type: {metric}")

        # Create set of available dimensions from `dimension` items in the metrics object
        for m in response["Metrics"]:
            avail_dimensions.extend(
                [(d["Name"], d["Value"]) for d in m["Dimensions"] if d]
            )

        if not req_dimensions.issubset(set(avail_dimensions)):
            raise InvalidDimension(
                f"No Metrics of type '{metric}' with Dimensions '{req_dimensions}'"
            )

        return True

    def _statistics_get(self):
        """Get metric statistics data

        Returns:
            Metric object with a list of Datapoints
        """

        query = self._query_make(self.cmdargs)
        return self.session.client("cloudwatch").get_metric_statistics(**query)

    def probe(self):
        """Query AWS CloudWatch for health data

        Returns:
            generator yielding nagiosplugin.Metric objects
        """

        response = self._statistics_get()

        if "Datapoints" not in response or not response["Datapoints"]:
            return []

        label = response["Label"]
        if label != self.cmdargs.metric:
            raise UnexpectedResponse(
                f"Unexpected Metric in Response. Got: {label}, Expected: {self.cmdargs.metric}"
            )

        stat_name = self.cmdargs.statistic.capitalize()
        for point in response["Datapoints"]:
            stat_val = point.get(stat_name)
            yield nagiosplugin.Metric(self.cmdargs.metric, stat_val)

    @property
    def name(self):
        return NAME
