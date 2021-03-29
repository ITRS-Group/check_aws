import warnings
from argparse import Action
from os import environ, path

from botocore.exceptions import NoCredentialsError


class DimensionsSerializer(Action):
    def __call__(self, parser, namespace, value, option_string=None):
        """Load dimensions

        Deserializes the given value into `namespace.dimensions`
        """

        if not value:
            return

        data = self.load(value)
        namespace.dimensions = list(data)

    @staticmethod
    def dump(data):
        """Serialize dimensions

        Args:
            data: Dict to serialize

        Returns:
            Comma-separated dimensions string
        """

        return " ({})".format(", ".join("{Name}={Value}".format(**d) for d in data))

    @staticmethod
    def load(value):
        """Deserialize dimensions

        Args:
            value: String to deserialize

        Returns:
            Generator yielding list of key-value items
        """

        for pair in value.split(","):
            k, v = pair.split("=")

            if not v:
                raise ValueError("Dimension {} value cannot be empty".format(k))

            yield dict(Name=k, Value=v)


class CredentialsFileSetter(Action):
    def __call__(self, parser, namespace, value, option_string=None):
        """Set credentials file

        Sets credentials file to use for authenticating with AWS.
        """

        if not value:
            # Use default ~/.aws/credentials
            value = path.join(path.expanduser("~"), ".aws", "credentials")

        if option_string == "--credentials":
            warnings.warn(
                "The --credentials option is DEPRECATED. "
                "Please use --credentials_file instead.",
                DeprecationWarning,
            )

        if not path.exists(value):
            # We want NoCredentialsError to be raised upon parsing CLI args if
            # there's an error, rather than when actually attempting to authenticate.
            raise NoCredentialsError

        # Boto3 only supports setting a custom credentials file via the env
        environ["AWS_SHARED_CREDENTIALS_FILE"] = value
