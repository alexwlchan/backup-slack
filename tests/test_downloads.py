# -*- encoding: utf-8
"""Test the functions for downloading."""

import json

from slack_history import downloaders


class TestDownloadUsernames(object):
    """Tests for `download_usernames`."""

    class MockSlack(object):
        usernames = {
            'U01000': 'marie_curie',
            'U02000': 'sophie_wilson',
            'U03000': 'grace_hopper',
        }

    slack = MockSlack()

    def test_download_usernames(self, slack, tmpdir):
        """Test `download_usernames` when there isn't an existing file."""
        path = tmpdir.join('users.json')
        assert not path.exists()

        # Download the user data
        downloaders.download_usernames(slack=self.slack, path=str(path))

        # Read data back from the file, and check it's correct
        assert json.loads(path.read())['U01000'] == 'marie_curie'

    def test_update_download_usernames(self, tmpdir):
        """Test `download_usernames` when there's an existing file."""
        path = tmpdir.join('users_existing.json')
        assert not path.exists()

        # Write some data to the file -- one which overlaps with data from
        # the mock Slack API, one that's new
        path.write(json.dumps({
            'U01000': 'maria_skłodowska',
            'U04000': 'vera_rubin',
        }))

        # Now download new username IDs from the Slack API
        downloaders.download_usernames(slack=self.slack, path=str(path))

        # Check the user ID that was in the original file but not the new API
        # data was preserved
        assert json.loads(path.read())['U04000'] == 'vera_rubin'

        # Check the user ID that was updated in the API response was updated
        assert json.loads(path.read())['U01000'] == 'marie_curie'


class TestDownloadHistory(object):

    history = [
        {
            'body': 'message 3',
            'ts': '300',
        },
        {
            'body': 'message 2',
            'ts': '200',
        },
        {
            'body': 'message 1',
            'ts': '100',
        },
    ]

    def test_download_history(self, tmpdir):
        """Test for `download_history` in a fresh file."""
        path = tmpdir.join('export.json')
        assert not path.exists()

        downloaders.download_history(
            channel_info='my_great_channel',
            history=self.history,
            path=str(path))

        assert path.exists()
        assert json.loads(path.read()) == {
            'channel': 'my_great_channel',
            'messages': self.history,
        }

    def test_download_history(self, tmpdir):
        """Test for `download_history` with a pre-existing file."""
        path = tmpdir.join('export.json')
        assert not path.exists()

        # First create a file with some messages
        downloaders.download_history(
            channel_info='my_great_channel',
            history=self.history,
            path=str(path))

        # This generator will return some more messages, including messages
        # that have already been saved.  It will error if we try to read
        # more than one message that has already been saved to disk.
        def new_history():
            yield {'body': 'message 5', 'ts': '500'}
            yield {'body': 'message 4', 'ts': '400'}
            yield {'body': 'message 3', 'ts': '300'}
            assert False, 'Tried to read too many already-saved messages'

        downloaders.download_history(
            channel_info='my_great_channel',
            history=new_history(),
            path=str(path))

        # Check that the new file contains five entries -- not six!
        assert len(json.loads(path.read())['messages']) == 5
