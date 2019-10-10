import pytest


def test_namespace_valid(invoke_cli):
    assert invoke_cli({"-n": "test"}).namespace == "test"
    assert invoke_cli({"-n": "test123"}).namespace == "test123"
    assert invoke_cli({"--namespace": "TEST"}).namespace == "TEST"
    assert invoke_cli({"--namespace": "TEST//ÅÄÖ__"}).namespace == "TEST//ÅÄÖ__"


def test_region_valid(invoke_cli):
    assert invoke_cli({"-r": "eu-west-2"}).region == "eu-west-2"
    assert invoke_cli({"-r": "ap-southeast-2"}).region == "ap-southeast-2"
    assert invoke_cli({"--region": "ap-south-1"}).region == "ap-south-1"


def test_statistic_valid(invoke_cli):
    assert invoke_cli({"-s": "Average"}).statistic == "Average"
    assert invoke_cli({"--statistic": "Sum"}).statistic == "Sum"


def test_statistic_invalid(invoke_cli):
    with pytest.raises(SystemExit):
        assert invoke_cli({"-s": "test"})

    with pytest.raises(SystemExit):
        assert invoke_cli({"--statistic": "test"})


def test_general_invalid(invoke_cli):
    with pytest.raises(SystemExit):
        assert invoke_cli({"--realm": "--invalid"})

    with pytest.raises(SystemExit):
        assert invoke_cli({"-n": "--INVALID"})

    with pytest.raises(SystemExit):
        assert invoke_cli({"-d": "-x"})


def test_region_invalid(invoke_cli):
    with pytest.raises(SystemExit):
        assert invoke_cli({"--real": "eu-west-2"})

    with pytest.raises(SystemExit):
        assert invoke_cli({"--realm": "invalid"})

    with pytest.raises(SystemExit):
        assert invoke_cli({"-r": "invalid"})


def test_dimensions_parsed(invoke_cli):
    assert invoke_cli({"-d": "test=test"}).dimensions == dict(test="test")
    assert invoke_cli({"--dimensions": "foo=bar"}).dimensions == dict(foo="bar")


def test_dimensions_parse_fail(invoke_cli):
    with pytest.raises(ValueError):
        assert invoke_cli({"-d": "test^test"})

    with pytest.raises(ValueError):
        assert invoke_cli({"-d": "test="})

    with pytest.raises(ValueError):
        assert invoke_cli({"--dimensions": "test"})
