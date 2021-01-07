import pytest

from botocore.exceptions import NoCredentialsError
from nagios_aws.consts import Default


def test_custom_file(cli):
    assert cli({"-C": "tests/input/credentials"})


def test_custom_falsy(cli):
    assert cli({"-C": ""}).credentials_file == Default.credentials_file.value


def test_default(cli):
    assert cli().credentials_file == Default.credentials_file.value


def test_non_file(resource):
    # with pytest.raises(NoCredentialsError):
    resource(
        overrides={
            "--profile": "test_non_section",
            "--credentials_file": "tests/input/non_existent_file",
        }
    )
