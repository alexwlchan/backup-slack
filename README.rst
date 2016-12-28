slack_history
=============

This is a tool for backing up your message history from Slack.

It uses the Slack API to download the history of your public/private
channels and direct message threads, and save them as a JSON file.
(The `data exports <https://get.slack.help/hc/en-us/articles/204897248>`_
provided by Slack only include messages sent in public channels.)
If you're using one of the paid tiers, this retrieves your complete
history.  For the free tiers, only the last 10,000 messages are accessible
through the Slack API.

*This tool is not created by, affiliated with, or supported by Slack Technologies, Inc.*

Installation
------------

To install slack_history, use ``pip``:

.. code-block:: console

   $ pip install slack_history

or `pipsi <https://github.com/mitsuhiko/pipsi>`_:

.. code-block:: console

   $ pipsi install slack_history

You can use Python 2.7 and Python 3.3+.

Usage
-----

You run the tool on the command-line, passing a `Slack API token
<https://api.slack.com/web>`_ for authentication:

.. code-block:: console

   $ slack_history --token='abcdef'

This saves a series of JSON files to the current directory.  To see other
options, run with the ``--help`` flag:

.. code-block:: console

   $ slack_history --help

License
-------

This project is licensed under the MIT license.
