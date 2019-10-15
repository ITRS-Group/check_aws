import pytest

from aws.cli import get_default_credentials_file


def test_namespace_valid(cli):
    assert cli({"-n": "test"}).namespace == "test"
    assert cli({"-n": "test123"}).namespace == "test123"
    assert cli({"--namespace": "TEST"}).namespace == "TEST"
    assert cli({"--namespace": "TEST//ÅÄÖ__"}).namespace == "TEST//ÅÄÖ__"


def test_region_valid(cli):
    assert cli({"-r": "eu-west-2"}).region == "eu-west-2"
    assert cli({"-r": "ap-southeast-2"}).region == "ap-southeast-2"
    assert cli({"--region": "ap-south-1"}).region == "ap-south-1"


def test_statistic_valid(cli):
    assert cli({"-s": "Average"}).statistic == "Average"
    assert cli({"--statistic": "Sum"}).statistic == "Sum"


def test_statistic_invalid(cli):
    with pytest.raises(SystemExit):
        assert cli({"-s": "test"})

    with pytest.raises(SystemExit):
        assert cli({"--statistic": "test"})


def test_general_invalid(cli):
    with pytest.raises(SystemExit):
        assert cli({"--region": "--invalid"})

    with pytest.raises(SystemExit):
        assert cli({"-n": "--INVALID"})

    with pytest.raises(SystemExit):
        assert cli({"-d": "-x"})


def test_region_invalid(cli):
    with pytest.raises(SystemExit):
        assert cli({"--real": "eu-west-2"})

    with pytest.raises(SystemExit):
        assert cli({"--realm": "invalid"})

    with pytest.raises(SystemExit):
        assert cli({"-r": "invalid"})


def test_dimensions_parsed(cli):
    assert cli({"-d": "test=test"}).dimensions == dict(test="test")
    assert cli({"--dimensions": "foo=bar"}).dimensions == dict(foo="bar")


def test_dimensions_empty(cli):
    assert cli({"-d": ""}).dimensions is None


def test_dimensions_parse_fail(cli):
    with pytest.raises(ValueError):
        assert cli({"-d": "test^test"})

    with pytest.raises(ValueError):
        assert cli({"-d": "test="})

    with pytest.raises(ValueError):
        assert cli({"--dimensions": "test"})


def test_custom_credentials_file(cli):
    assert cli({"-C": "tests/input/credentials"})


def test_custom_credentials_file_fail(cli):
    with pytest.raises(OSError):
        assert cli({"-C": "tests/input/foobar.txt"})


def test_custom_credentials_default(cli):
    assert cli({"-C": ""}).credentials_file == get_default_credentials_file()

