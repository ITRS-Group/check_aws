import nagiosplugin

from nagios_aws.cli.actions import DimensionsSerializer


class CloudWatchSummary(nagiosplugin.Summary):
    def __init__(self, namespace, metric, dimensions=None):
        self.namespace = namespace
        self.metric = metric
        self.dimensions = dimensions

    def get_message(self, result):
        result_text = result[0].metric.value

        msg = "Metric {0}:{1} {2}".format(
            self.namespace,
            self.metric,
            result_text
        )

        if self.dimensions:
            msg += DimensionsSerializer.dump(self.dimensions)

        return msg

    def ok(self, result):
        return self.get_message(result)

    def problem(self, result):
        return self.get_message(result)
