# -*- encoding: utf-8
"""Tests for slack_history.api."""


def test_messages_always_come_newest_first(slack):
    """No matter which order messages are returned from the Slack API,
    they are passed to the caller with the newest message first.
    """
    slack.slack.channels.mock_history = [
        {
            'ts': '100',
            'msg': 'I am the first message',
            'user': 'U01000',
        },
        {
            'ts': '400',
            'msg': 'I am the last message',
            'user': 'U01000',
        },
        {
            'ts': '300',
            'msg': 'I am the penultimate message',
            'user': 'U03000',
        },
        {
            'ts': '200',
            'msg': 'I am the second message',
            'user': 'U02000',
        },
    ]

    history = list(slack.channel_history(channel={'id': 1}))
    assert [m['ts'] for m in history] == ['400', '300', '200', '100']


def test_dm_threads_have_usernames(slack):
    """When getting a list of DM threads, they include a human-readable
    username (not user ID) for each thread.
    """
    slack.slack.im.mock_list = {
        'ims': [
            {'user': 'U01000'},
            {'user': 'U02000'},
        ],
    }

    for thread in slack.dm_threads():
        assert 'username' in thread
