# -*- encoding: utf-8

import argparse


def parse_args(prog, version):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='A tool for downloading message history from Slack.  This '
                    'tool downloads the message history for all your public '
                    'channels, private channels, and direct message threads.',
        epilog='If your team is on the free Slack plan, this tool can '
               'download your last 10,000 messages.  If your team is on a paid '
               'plan, this can download your entire account history.',
        prog=prog)

    parser.add_argument(
        '--version', action='version', version='%(prog)s ' + version)
    parser.add_argument(
        '--outdir', help='output directory', default='.')
    parser.add_argument(
        '--token', required=True,
        help='Slack API token; obtain from https://api.slack.com/web')

    return parser.parse_args()
