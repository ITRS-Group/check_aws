import argparse


class DimensionParser(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        kvs = {}

        if not values:
            return

        for pair in values.split(','):
            k, v = pair.split('=')
            if not v:
                raise ValueError("Dimension {} value cannot be empty".format(k))

            kvs[k] = v

        setattr(namespace, self.dest, kvs)
