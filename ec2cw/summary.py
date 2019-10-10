import nagiosplugin


class CloudWatchSummary(nagiosplugin.Summary):
    def __init__(self, namespace, metric, dimensions=None):
        self._msg = "Metric {}:{}".format(namespace, metric)

        if dimensions:
            # Convert dimensions back into str {x: y} => x=y for a better human experience.
            self._msg += " ({})".format(', '.join("{0}={1}".format(*d) for d in dimensions.items()))

    def ok(self, results):
        return self._msg

    def problem(self, results):
        return self._msg
