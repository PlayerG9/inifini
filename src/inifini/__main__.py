# -*- coding=utf-8 -*-
r"""

"""
import sys
import argparse as ap
from . import __description__, __version__


parser = ap.ArgumentParser(
    prog='inifini',
    description=__description__,
    formatter_class=ap.ArgumentDefaultsHelpFormatter
)
parser.add_argument('-v', '--version', action='version', version=__version__)


def main():
    parser.parse_args()
    print("Under Development", file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    main()
