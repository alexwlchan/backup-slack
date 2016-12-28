# -*- encoding: utf-8

import argparse


def parse_args(prog, version):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(prog=prog)

    parser.add_argument(
        '--version', action='version', version='%(prog)s ' + version)
    parser.add_argument(
        '--outdir', help='output directory', default='.')

    return parser.parse_args()
