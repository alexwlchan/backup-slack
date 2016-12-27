# -*- encoding: utf-8

import datetime
import errno
import os
import time


def mkdir_p(path):
    """Create a directory if it does not already exist.

    http://stackoverflow.com/a/600612/1558022

    """
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def slack_ts_to_datetime(ts):
    """Try to convert a 'ts' value from the Slack into a UTC datetime."""
    time_struct = time.localtime(float(ts))
    return datetime.datetime.fromtimestamp(time.mktime(time_struct))
