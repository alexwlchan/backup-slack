# -*- encoding: utf-8
"""Download channel history from Slack."""

import json
import operator
import os

from .api import SlackHistory
from .utils import mkdir_p

__version__ = '1.0.0'


USERNAMES = 'users.json'
PUBLIC_CHANNELS = 'channels'


def download_public_channel(slack, channel):
    """Download the message history for a specific public channel."""
    mkdir_p(PUBLIC_CHANNELS)
    path = os.path.join(PUBLIC_CHANNELS, '%s.json' % channel['name'])
    try:
        with open(path) as infile:
            existing_messages = json.load(infile)['messages']
    except OSError:
        existing_messages = []

    for msg in slack.channel_history(channel=channel):
        if msg in existing_messages:
            break
        existing_messages.append(msg)

    existing_messages = sorted(existing_messages,
                               key=operator.itemgetter('ts'))
    data = {
        'channel': channel,
        'messages': existing_messages,
    }
    json_str = json.dumps(data, indent=2, sort_keys=True)
    with open(path, 'w') as outfile:
        outfile.write(json_str)


def download_public_channels(slack):
    """Download the message history for the public channels where this user
    is logged in.
    """
    for channel in slack.channels():
        if channel['is_member']:
            download_public_channel(slack=slack, channel=channel)


def main():
    slack = SlackHistory(token=open('token.txt').read().strip())

    with open(USERNAMES, 'w') as f:
        f.write(json.dumps(slack.usernames, indent=2, sort_keys=True))
    print('Written username list to %s' % USERNAMES)

    download_public_channels(slack)
    print('Written public channel histories to %s' % PUBLIC_CHANNELS)
