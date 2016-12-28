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

    usernames = os.path.join(args.outdir, USERNAMES)
    print('Saving username list to %s' % usernames)
    download_usernames(slack, path=usernames)

    public_channels = os.path.join(args.outdir, PUBLIC_CHANNELS)
    print('Saving public channels to %s' % public_channels)
    download_public_channels(slack, outdir=public_channels)

    private_channels = os.path.join(args.outdir, PRIVATE_CHANNELS)
    print('Saving private channels to %s' % private_channels)
    download_private_channels(slack, outdir=private_channels)

    direct_messages = os.path.join(args.outdir, DIRECT_MESSAGES)
    print('Saving direct messages to %s' % direct_messages)
    download_dm_threads(slack, outdir=direct_messages)
