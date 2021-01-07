import pytest

from nagios_aws.consts import Default


def test_custom_file(cli):
    assert cli({"-C": "tests/input/credentials"})


def test_custom_falsy(cli):
    assert cli({"-C": ""}).credentials_file == Default.credentials_file.value


def test_default(cli):
    assert cli().credentials_file == Default.credentials_file.value


def test_section_exists(resource):
    options = resource(
        overrides={"--credentials": "tests/input/credentials", "--profile": "default"}
    ).get_credentials()

    assert all([opt for opt in options.values()])


def test_non_section(resource):
    options = resource(
        overrides={
            "--profile": "test_non_section",
            "--credentials": "tests/input/credentials",
        }
    ).get_credentials()

    assert not all([opt for opt in options.values()])


def test_non_file(resource):
    with pytest.raises(FileNotFoundError):
        resource(
            overrides={
                "--profile": "test_non_section",
                "--credentials": "tests/input/non_existent_file",
            }
        ).get_credentials()
