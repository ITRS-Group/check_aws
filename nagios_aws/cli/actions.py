import warnings

from os import environ
from argparse import Action

from nagios_aws.consts import Default


class DimensionsSerializer(Action):
    """Performs (de)serialization of Dimensions"""

    def __call__(self, parser, namespace, value, option_string=None):
        if not value:
            return

        data = self.load(value)
        namespace.dimensions = list(data)

    @staticmethod
    def dump(data):
        return " ({})".format(", ".join("{0}={1}".format(*d) for d in data.items()))

    @staticmethod
    def load(value):
        for pair in value.split(","):
            k, v = pair.split("=")

            if not v:
                raise ValueError("Dimension {} value cannot be empty".format(k))

            yield dict(Name=k, Value=v)


class CredentialsFileHandler(Action):
    def __call__(self, parser, namespace, value, option_string=None):
        if not value:
            value = getattr(Default, self.dest).value

        if option_string == "--credentials":
            warnings.warn(
                "The credentials option is DEPRECATED. "
                "Please use credentials_file instead."
            )

        # Boto3 only supports setting a custom credentials file via the env
        environ["AWS_SHARED_CREDENTIALS_FILE"] = value
