import sys

from nagiosplugin import guarded, Check
from nagios_aws import parse_cmdline

from .target import Target


@guarded(verbose=False)
def main():
    args = parse_cmdline(sys.argv[1:])
    Check(*Target(args)).main(verbose=args.verbosity > 0)


if __name__ == "__main__":
    main()
