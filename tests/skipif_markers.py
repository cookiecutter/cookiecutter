#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
skipif_markers
--------------

Contains pytest skipif markers to be used in the suite.
"""

import pytest
import os


try:
    os.environ[u'TRAVIS']
except KeyError:
    travis = False
else:
    travis = True

try:
    os.environ[u'DISABLE_NETWORK_TESTS']
except KeyError:
    no_network = False
else:
    no_network = True

skipif_travis = pytest.mark.skipif(
    travis, reason='Works locally with tox but fails on Travis.'
)

skipif_no_network = pytest.mark.skipif(
    no_network, reason='Needs a network connection to GitHub/Bitbucket.'
)
