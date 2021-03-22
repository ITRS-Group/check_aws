from argparse import Namespace

import pytest

from nagios_aws import CloudWatchResource, parse_cmdline
from nagios_aws.consts import InputDefault
from nagios_aws.target import Target

METRICS_DEFAULT = {
    "Metrics": [
        {
            "Namespace": "AWS/EC2",
            "MetricName": "CPUCreditUsage",
            "Dimensions": [],
        }
    ]
}


class MockResource(CloudWatchResource):
    def __init__(self, cmdargs, response=None, metrics_available=None):
        self._metrics_available = metrics_available
        self._response = response or {}
        super(MockResource, self).__init__(cmdargs)

    def _metrics_get(self, **kwargs):
        if isinstance(self._metrics_available, list):
            metrics = self._metrics_available.pop(0)
        else:
            metrics = self._metrics_available

        return metrics

    def _statistics_get(self, *args, **kwargs):
        return self._response


def make_namespace(cmdargs):
    cfg = InputDefault().__dict__
    cfg.update(cmdargs or {})
    return Namespace(**cfg)


@pytest.fixture
def cli():
    def go(cli_args):
        options = []

        for k, v in cli_args.items():
            options.extend([k, v])

        return parse_cmdline(options)

    yield go


@pytest.fixture
def resource():
    def go(cmdargs=None, response=None, metrics_available=None):
        return MockResource(
            make_namespace(cmdargs), response, metrics_available or METRICS_DEFAULT
        )

    yield go


@pytest.fixture
def target(resource):
    def go(cmdargs=None, response=None):
        return Target(
            make_namespace(cmdargs), resource_cls=MockResource, response=response
        )

    yield go
