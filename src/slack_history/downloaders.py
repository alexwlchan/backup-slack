#!/usr/bin/env python
# -*- encoding: utf-8
"""Functions for downloading Slack API data to JSON files on disk."""

import operator
import os
import json

from .utils import mkdir_p


def download_public_channel(slack, channel, path):
    """Download the message history for a specific public channel."""
    mkdir_p(os.path.dirname(path))
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


def download_public_channels(slack, outdir):
    """Download the message history for the public channels where this user
    is logged in.
    """
    for channel in slack.channels():
        if channel['is_member']:
            path = os.path.join(outdir, '%s.json' % channel['name'])
            download_public_channel(slack=slack, channel=channel, path=path)


def download_usernames(slack, path):
    """Download the username history from Slack."""
    try:
        with open(path) as infile:
            usernames = json.load(infile)
    except OSError:
        usernames = {}

    usernames.update(slack.usernames)
    json_str = json.dumps(usernames, indent=2, sort_keys=True)
    with open(path, 'w') as outfile:
        outfile.write(json_str)
