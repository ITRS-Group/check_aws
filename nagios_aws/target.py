from nagiosplugin import ScalarContext
from nagios_aws import CloudWatchResource, CloudWatchSummary


class Target:
    def __init__(self, cfg, resource_cls=CloudWatchResource, **resource_kwargs):
        self.resource = resource_cls(cfg, **resource_kwargs)
        self.summary = CloudWatchSummary(
            namespace=cfg.namespace, metric=cfg.metric, dimensions=cfg.dimensions
        )
        self.context = ScalarContext(cfg.metric, cfg.warning, cfg.critical)

    def __iter__(self):
        yield self.resource
        yield self.summary
        yield self.context
