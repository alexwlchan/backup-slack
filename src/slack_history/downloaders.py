#!/usr/bin/env python
# -*- encoding: utf-8
"""Functions for downloading Slack API data to JSON files on disk."""

import operator
import os
import json

from .utils import mkdir_p


def download_history(channel_info, history, path):
    """Download the message history and save it to a JSON file."""
    mkdir_p(os.path.dirname(path))
    try:
        with open(path) as infile:
            existing_messages = json.load(infile)['messages']
    except OSError:
        existing_messages = []

    # TODO: For convenience, the messages yielded from `history` usually
    # have more than just the raw Slack API response: in particular, they have
    # a username and a date string.  If the username and/or timestamp format
    # changes, we could inadvertently save duplicate messages.
    for msg in history:
        if msg in existing_messages:
            break
        existing_messages.append(msg)

    # Newest messages appear at the top of the file
    existing_messages = sorted(existing_messages,
                               key=operator.itemgetter('ts'),
                               reverse=True)
    data = {
        'channel': channel_info,
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
            history = slack.channel_history(channel=channel)
            path = os.path.join(outdir, '%s.json' % channel['name'])
            download_history(channel_info=channel, history=history, path=path)


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


def download_dm_threads(slack, outdir):
    """Download the message history for this user's direct message threads."""
    for thread in slack.dm_threads():
        history = slack.dm_thread_history(thread=thread)
        path = os.path.join(outdir, '%s.json' % thread['username'])
        download_history(channel_info=thread, history=history, path=path)


def download_private_channels(slack, outdir):
    """Download the message history for the private channels where this user
    is logged in.
    """
    for thread in slack.private_channels():
        history = slack.private_channel_history(thread=thread)
        path = os.path.join(outdir, '%s.json' % thread['username'])
        download_history(channel_info=thread, history=history, path=path)
