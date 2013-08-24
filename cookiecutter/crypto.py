#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.crypto
-------------------

Functions for generating secret keys and other crypto-related items.
"""

from __future__ import unicode_literals
import random

CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

system_random = None
try:
    system_random = random.SystemRandom()
except NotImplementedError:
    import warnings
    warnings.warn("A secure pseudo-random number generator is not available "
                  "on your system. The value 'CHANGEME!!!' will be used"
                  " instead.")


def get_secret_key(system_random=system_random):
    """
    Returns a 50 character securely generated random string.
    """
    if system_random is None:
        # This return CHANGEME, and when combined with the warning during
        # import encourages the cookiecutter user to come up with their
        # own random keys
        return 'CHANGEME!!!'

    return ''.join([random.choice(CHARS) for i in range(50)])
