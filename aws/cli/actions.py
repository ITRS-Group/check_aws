from argparse import Action

from aws.consts import Default


class DimensionsSerializer(Action):
    """Performs (de)serialization of Dimensions"""

    def __call__(self, parser, namespace, value, option_string=None):
        if not value:
            return

        data = self.load(value)
        setattr(namespace, self.dest, dict(data))

    @staticmethod
    def dump(data):
        return " ({})".format(', '.join("{0}={1}".format(*d) for d in data.items()))

    @staticmethod
    def load(value):
        for pair in value.split(','):
            k, v = pair.split('=')

            if not v:
                raise ValueError("Dimension {} value cannot be empty".format(k))

            yield k, v


class CredentialsFileResolver(Action):
    """Credentials file resolver

    Ensures a falsy credentials file argument is set to its field's default value.

    This is mainly to provide compatibility with the various "metadata" packs in OP5 Monitor
    without using wrapper hacks.
    """

    def __call__(self, parser, namespace, value, option_string=None):
        if not value:
            value = Default.credentials_file.value

        setattr(namespace, self.dest, value)
