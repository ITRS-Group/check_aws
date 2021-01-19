from argparse import Namespace

import pytest

from nagios_aws import CloudWatchResource, consts, parse_cmdline
from nagios_aws.target import Target


class MockResource(CloudWatchResource):
    def __init__(self, cfg, response=None):
        self.__response = response or {}
        super(MockResource, self).__init__(cfg)

    def _send(self, *args, **kwargs):
        return self.__response


def make_namespace(payload):
    """Creates new namespace using default config merged with given payload"""

    cfg = consts.InputDefault().__dict__
    cfg.update(payload or {})
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
    def go(payload=None, response=None):
        return MockResource(make_namespace(payload), response)

    yield go


@pytest.fixture
def target(resource):
    def go(payload=None, response=None):
        return Target(
            make_namespace(payload), resource_cls=MockResource, response=response
        )

    yield go
