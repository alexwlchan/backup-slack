# -*- encoding: utf-8
"""Download channel history from Slack."""

import os
import sys

from .api import SlackHistory
from .cli import parse_args
from .downloaders import (
    download_dm_threads, download_private_channels, download_public_channels,
    download_usernames)
from .utils import mkdir_p

__version__ = '1.0.0'


USERNAMES = 'users.json'
DIRECT_MESSAGES = 'direct_messages'
PUBLIC_CHANNELS = 'channels'
PRIVATE_CHANNELS = 'private_channels'


def main():
    args = parse_args(prog=os.path.basename(sys.argv[0]), version=__version__)

    slack = SlackHistory(token=open('token.txt').read().strip())

    mkdir_p(args.outdir)
    os.chdir(args.outdir)

    download_usernames(slack, path=USERNAMES)
    print('Saved username list to %s' % USERNAMES)

    download_public_channels(slack, outdir=PUBLIC_CHANNELS)
    print('Saved public channels to %s' % PUBLIC_CHANNELS)

    download_dm_threads(slack, outdir=DIRECT_MESSAGES)
    print('Saved direct messages to %s' % DIRECT_MESSAGES)

    download_private_channels(slack, outdir=PRIVATE_CHANNELS)
    print('Saved private channels to %s' % PRIVATE_CHANNELS)
