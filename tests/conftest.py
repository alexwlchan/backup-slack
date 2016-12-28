# -*- encoding: utf-8
"""Mocks for the tests.

Coming up with mocked out versions of slacker.Slacker turns out to be
quite fiddly, and I've been doing a fairly low-level patch of the
HTTP requests that come off the wire from the Slack API.  There's probably
a much nicer way to do this, but this seems to work for now.
"""

import json

import mock
import pytest
import slacker

import slack_history


class MockBaseAPI(slacker.BaseAPI):

    def get(self, api, *args, **kwargs):
        return slacker.Response(json.dumps(self.mock_get))

    def history(self, *args, **kwargs):
        mock_history = {
            'ok': 'true',
            'messages': self.mock_history,
            'has_more': False,
        }
        return slacker.Response(json.dumps(mock_history))

    def list(self, *args, **kwargs):
        if 'ok' not in self.mock_list:
            self.mock_list['ok'] = 'true'
        return slacker.Response(json.dumps(self.mock_list))


def mock_class(cls):
    class MockedClass(MockBaseAPI, cls):
        pass
    return MockedClass()


class MockUsers(MockBaseAPI):

    mock_get = {
        'ok': 'true'
    }

    mock_list = {
        'ok': 'true',
        'members': [
            {
                'id': 'U01000',
                'name': 'marie_curie',
            },
            {
                'id': 'U02000',
                'name': 'sophie_wilson',
            },
            {
                'id': 'U03000',
                'name': 'grace_hopper',
            },
        ],
    }


class MockSlack(slacker.Slacker):
    """A mock version of the Slack API"""
    def __init__(self, *args, **kwargs):
        super(MockSlack, self).__init__(*args, **kwargs)
        self.channels = mock_class(slacker.Channels)
        self.im = mock_class(slacker.IM)
        self.users = MockUsers()


@pytest.fixture
def slack():
    with mock.patch('slack_history.api.slacker.Slacker', MockSlack):
        return slack_history.SlackHistory(token='abc123')
