#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import os
import re

from setuptools import find_packages, setup


# Get the version.  Stolen from Cory Benfield.
version_regex = r'__version__ = ["\']([^"\']*)["\']'
with open('src/slack_history/__init__.py', 'r') as f:
    text = f.read()
    match = re.search(version_regex, text)

    if match:
        version = match.group(1)
    else:
        raise RuntimeError("No version number found!")


def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))


SOURCE = local_file('src')
README = local_file('README.rst')
long_description = codecs.open(README, encoding='utf-8').read()


setup(
    name='slack_history',
    version=version,
    description='A tool for backing up history from Slack',
    long_description=long_description,
    url='https://github.com/alexwlchan/slack_history',
    author='Alex Chan',
    author_email='alex@alexwlchan.net',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
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
    packages=find_packages(SOURCE),
    package_dir={'': SOURCE},
    install_requires=[
        'slacker>=0.9.30, <1',
    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'slack_history=slack_history:main',
        ],
    },
)
