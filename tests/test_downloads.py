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

    def test_download_usernames(self, tmpdir):
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
