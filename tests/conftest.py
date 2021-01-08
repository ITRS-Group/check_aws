import pytest

from nagios_aws import parse_cmdline, CloudWatchResource


@pytest.fixture
def cli():
    def _loaded_cli(opts_override=None):
        """Enables easy testing of the EC2CW CLI"""

        # Default opts dictionary, for convenience
        opts_map = {
            "--namespace": "AWS/VPN",
            "--region": "eu-west-1",
            "--metric": "TunnelState",
            "--unit": "Bytes",
        }

        # Override defaults
        opts_map.update(opts_override or {})
        opts_lst = []

        # Argparse expects a list as input: convert
        for k, v in opts_map.items():
            opts_lst.extend([k, v])

        return parse_cmdline(opts_lst)

    return _loaded_cli


@pytest.fixture
def resource(cli):
    def _loaded_resource(overrides=None):
        cfg = cli(opts_override=overrides)
        return CloudWatchResource(cfg)

    return _loaded_resource
