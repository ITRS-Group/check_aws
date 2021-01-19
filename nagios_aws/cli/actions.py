import warnings
from argparse import Action
from os import environ, path

from botocore.exceptions import NoCredentialsError


class DimensionsSerializer(Action):
    """Performs (de)serialization of Dimensions"""

    def __call__(self, parser, namespace, value, option_string=None):
        if not value:
            return

        data = self.load(value)
        namespace.dimensions = list(data)

    @staticmethod
    def dump(data):
        return " ({})".format(", ".join("{Name}={Value}".format(**d) for d in data))

    @staticmethod
    def load(value):
        for pair in value.split(","):
            k, v = pair.split("=")

            if not v:
                raise ValueError("Dimension {} value cannot be empty".format(k))

            yield dict(Name=k, Value=v)


class CredentialsFileParser(Action):
    def __call__(self, parser, namespace, value, option_string=None):
        if not value:
            value = path.join(path.expanduser("~"), ".aws", "credentials")

        if option_string == "--credentials":
            warnings.warn(
                "The --credentials option is DEPRECATED. "
                "Please use --credentials_file instead.",
                DeprecationWarning,
            )

        if not path.exists(value):
            # We want NoCredentialsError to be raised upon parsing CLI args, rather
            # than when actually attempting to authenticate.
            raise NoCredentialsError

        # Boto3 only supports setting a custom credentials file via the env
        environ["AWS_SHARED_CREDENTIALS_FILE"] = value
