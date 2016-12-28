# -*- encoding: utf-8
"""Wrappers for the Slack API."""

import slacker

from .utils import slack_ts_to_datetime


class SlackHistory(object):

    def __init__(self, *args, **kwargs):
        self.slack = slacker.Slacker(*args, **kwargs)
        self.usernames = self._fetch_user_mapping()

    def _get_history(self, channel_class, channel_id):
        """Returns the message history for a channel, group or DM thread."""
        # This wraps the `channels.history`, `groups.history` and `im.history`
        # methods from the Slack API, which can return up to 1000 messages
        # at once.
        #
        # Rather than spooling the entire history into a list before
        # returning, we pass messages to the caller as soon as they're
        # retrieved.  This means the caller can choose to exit early (and save
        # API calls) if they turn out not to want older messages, for example,
        # if they already have a copy of those locally.
        last_timestamp = None
        while True:
            response = channel_class.history(channel=channel_id,
                                             latest=last_timestamp,
                                             oldest=0,
                                             count=1000)
            for msg in response.body['messages']:
                last_timestamp = msg['ts']
                msg['date'] = str(slack_ts_to_datetime(msg['ts']))
                msg['username'] = self.usernames[msg['user']]
                yield msg
            if not response.body['has_more']:
                return

    def _fetch_user_mapping(self):
        """Gets a mapping of user IDs to usernames."""
        return {
            u['id']: u['name']
            for u in self.slack.users.list().body['members']}

    def channels(self):
        """Returns a list of public channels."""
        return self.slack.channels.list().body['channels']

    def channel_history(self, channel):
        """Returns the message history for a channel."""
        return self._get_history(self.slack.channels, channel_id=channel['id'])

    def dm_threads(self):
        """Returns a list of direct message threads."""
        threads = []
        for t in self.slack.im.list().body['ims']:
            t['username'] = self.usernames[t['user']]
            threads.append(t)
        return threads

    def dm_thread_history(self, thread):
        """Returns the message history for a direct message thread."""
        return self._get_history(self.slack.im, channel_id=thread['id'])
