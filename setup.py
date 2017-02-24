#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import os
import re

from setuptools import find_packages, setup


# Get the version.  Stolen from Cory Benfield.
version_regex = r'__version__ = ["\']([^"\']*)["\']'
with open('backup_slack.py',) as f:
    text = f.read()
    match = re.search(version_regex, text)

    if match:
        version = match.group(1)
    else:
        raise RuntimeError("No version number found!")


def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))


README = local_file('README.rst')
long_description = codecs.open(README, encoding='utf-8').read()


setup(
    name='backup_slack',
    version=version,
    description='A script for backing up message history from Slack',
    long_description=long_description,
    url='https://github.com/alexwlchan/backup-slack',
    author='Alex Chan',
    author_email='alex@alexwlchan.net',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=[
        'slacker>=0.9.30, <1',
    ],
    entry_points={
        'console_scripts': [
            'backup_slack=backup_slack:main',
        ],
    },
)
