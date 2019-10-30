import nagiosplugin

from aws.cli.actions import DimensionsSerializer


class CloudWatchSummary(nagiosplugin.Summary):
    def __init__(self, namespace, metric, dimensions=None):
        self._msg = "Metric {}:{}".format(namespace, metric)

        if dimensions:
            self._msg += DimensionsSerializer.dump(dimensions)

    def ok(self, _):
        return self._msg

    def problem(self, _):
        return self._msg
