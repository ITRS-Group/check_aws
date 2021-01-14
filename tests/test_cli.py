import pytest

from botocore.exceptions import NoCredentialsError
from nagios_aws.consts import InputDefault

CLI_DEFAULTS = {
    "--namespace": "AWS/VPN",
    "--region": "eu-west-1",
    "--metric": "",
    "--unit": "Count",
}


def test_custom_file(cli):
    assert cli({**CLI_DEFAULTS, "-C": "tests/input/credentials"})


def test_custom_falsy(cli):
    assert (
        cli({**CLI_DEFAULTS, "-C": ""}).credentials_file
        == InputDefault.credentials_file
    )


def test_default(cli):
    assert cli(CLI_DEFAULTS).credentials_file == InputDefault.credentials_file


def test_non_file(cli):
    with pytest.raises(NoCredentialsError):
        cli({**CLI_DEFAULTS, "--credentials_file": "/no/such/file"})


def test_namespace_valid(cli):
    assert cli({**CLI_DEFAULTS, "-n": "test"}).namespace == "test"
    assert cli({**CLI_DEFAULTS, "-n": "test123"}).namespace == "test123"
    assert cli({**CLI_DEFAULTS, "--namespace": "TEST"}).namespace == "TEST"
    assert (
        cli({**CLI_DEFAULTS, "--namespace": "TEST//ÅÄÖ__"}).namespace == "TEST//ÅÄÖ__"
    )


def test_region_valid(cli):
    assert cli({**CLI_DEFAULTS, "-r": "eu-west-2"}).region == "eu-west-2"
    assert cli({**CLI_DEFAULTS, "-r": "ap-southeast-2"}).region == "ap-southeast-2"
    assert cli({**CLI_DEFAULTS, "--region": "ap-south-1"}).region == "ap-south-1"


def test_statistic_valid(cli):
    assert cli({**CLI_DEFAULTS, "-s": "Average"}).statistic == "Average"
    assert cli({**CLI_DEFAULTS, "--statistic": "Sum"}).statistic == "Sum"


def test_statistic_invalid(cli):
    with pytest.raises(SystemExit):
        cli({**CLI_DEFAULTS, "-s": "test"})

    with pytest.raises(SystemExit):
        cli({**CLI_DEFAULTS, "--statistic": "test"})


def test_general_invalid(cli):
    with pytest.raises(SystemExit):
        cli({**CLI_DEFAULTS, "--region": "--invalid"})

    with pytest.raises(SystemExit):
        cli({**CLI_DEFAULTS, "-n": "--INVALID"})

    with pytest.raises(SystemExit):
        cli({**CLI_DEFAULTS, "-d": "-x"})


def test_region_invalid(cli):
    with pytest.raises(SystemExit):
        cli({**CLI_DEFAULTS, "--real": "eu-west-2"})

    with pytest.raises(SystemExit):
        cli({**CLI_DEFAULTS, "--realm": "invalid"})

    with pytest.raises(SystemExit):
        cli({**CLI_DEFAULTS, "-r": "invalid"})


def test_dimensions_parsed(cli):
    assert cli({**CLI_DEFAULTS, "-d": "foo=bar"}).dimensions == [
        dict(Name="foo", Value="bar")
    ]
    assert cli({**CLI_DEFAULTS, "--dimensions": "foo=bar"}).dimensions == [
        dict(Name="foo", Value="bar")
    ]


def test_dimensions_empty(cli):
    assert cli({**CLI_DEFAULTS, "-d": ""}).dimensions == tuple()


def test_dimensions_parse_fail(cli):
    with pytest.raises(ValueError):
        cli({**CLI_DEFAULTS, "-d": "test^test"})

    with pytest.raises(ValueError):
        cli({**CLI_DEFAULTS, "-d": "test="})

    with pytest.raises(ValueError):
        cli({**CLI_DEFAULTS, "--dimensions": "test"})
