# -*- encoding: utf-8
"""Tests for slack_history.utils."""

import pytest

from slack_history import utils


def test_mkdir_p_success(tmpdir):
    """Test the `mkdir_p` function works correctly."""
    # Choose a directory, and check it doesn't already exist
    test_dir = tmpdir.join('test_mkdir_p')
    assert not test_dir.exists()

    # Create the directory with `mkdir_p`, and check it exists
    utils.mkdir_p(str(test_dir))
    assert test_dir.exists()

    # Call `mkdir_p` a second time, and check it doesn't crash
    utils.mkdir_p(str(test_dir))


def test_mkdir_p_failure(tmpdir):
    """If `os.makedirs()` fails for a reason other than the directory already
    existing, an appropriate exception is raised.
    """
    # One way to induce this location is to have a _file_, not a directory,
    # at the chosen location.
    test_file = tmpdir.join('test_mkdir_p.txt')
    test_file.write('')

    with pytest.raises(OSError) as err:
        utils.mkdir_p(str(test_file))
    assert 'File exists' in err.value.args[1]


@pytest.mark.parametrize('ts, date_string', [
    ('1462574433.000021', '2016-05-06 23:40:33')
])
def test_slack_ts_to_datetime(ts, date_string):
    assert str(utils.slack_ts_to_datetime(ts) == date_string)
