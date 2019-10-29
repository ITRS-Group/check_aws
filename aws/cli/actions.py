from argparse import Action


class DimensionsSerializer(Action):
    """Performs Dimensions serialization"""

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
