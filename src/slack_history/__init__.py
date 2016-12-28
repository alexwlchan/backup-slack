# -*- encoding: utf-8
"""Download channel history from Slack."""

from .api import SlackHistory
from .downloaders import (
    download_dm_threads, download_public_channels, download_usernames)

__version__ = '1.0.0'


USERNAMES = 'users.json'
DIRECT_MESSAGES = 'direct_messages'
PUBLIC_CHANNELS = 'channels'


def main():
    slack = SlackHistory(token=open('token.txt').read().strip())

    download_usernames(slack, path=USERNAMES)
    print('Saved username list to %s' % USERNAMES)

    download_public_channels(slack, outdir=PUBLIC_CHANNELS)
    print('Saved public channels to %s' % PUBLIC_CHANNELS)

    download_dm_threads(slack, outdir=DIRECT_MESSAGES)
    print('Saved direct messages to %s' % DIRECT_MESSAGES)
