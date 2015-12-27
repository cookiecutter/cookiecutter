#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
skipif_markers
--------------

Contains pytest skipif markers to be used in the suite.
"""

import pytest
import os

from cookiecutter import vcs


travis = not not os.environ.get(u'TRAVIS', False)
no_network = not not os.environ.get(u'DISABLE_NETWORK_TESTS', False)
no_hg = vcs.is_vcs_installed('hg'),


skipif_travis = pytest.mark.skipif(
    travis, reason='Works locally with tox but fails on Travis.'
)

skipif_no_network = pytest.mark.skipif(
    no_network, reason='Needs a network connection to GitHub/Bitbucket.'
)

skipif_no_hg = pytest.mark.skipif(
    no_hg, reason='"hg" is not installed"'
)
