from nagiosplugin import ScalarContext

from check_aws import CloudWatchResource, CloudWatchSummary


class Target:
    def __init__(self, cmdargs, resource_cls=CloudWatchResource, **resource_kwargs):
        self.resource = resource_cls(cmdargs, **resource_kwargs)
        self.summary = CloudWatchSummary(
            namespace=cmdargs.namespace,
            metric=cmdargs.metric,
            dimensions=cmdargs.dimensions,
        )
        self.context = ScalarContext(cmdargs.metric, cmdargs.warning, cmdargs.critical)

    def __iter__(self):
        yield self.resource
        yield self.summary
        yield self.context
