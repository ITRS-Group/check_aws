import sys

from nagiosplugin import Check, guarded

from check_aws import parse_cmdline

from .target import Target


@guarded
def main():
    args = parse_cmdline(sys.argv[1:])
    Check(*Target(args)).main(verbose=args.verbosity)


if __name__ == "__main__":
    main()
