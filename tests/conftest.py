import pytest

from ec2cw.cli import parse_cmdline


@pytest.fixture
def invoke_cli():
    def _loaded(opts_override=None):
        """Enables easy testing of the EC2CW CLI"""

        # Default opts dictionary, for convenience.
        opts_map = {
            "--namespace": "AWS/VPN",
            "--region": "eu-west-1",
            "--metric": "TunnelState"
        }

        # Override defaults
        opts_map.update(opts_override or {})
        opts_lst = []

        # Argparse expects a list as input: convert.
        for k, v in opts_map.items():
            opts_lst.extend([k, v])

        return parse_cmdline(opts_lst)

    return _loaded
