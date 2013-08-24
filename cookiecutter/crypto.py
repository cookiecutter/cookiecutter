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


def get_secret_key(length=50, system_random=system_random):
    """
    :param length: The length of the returned character string. Defaults to 50.
    :paramtype length: int
    :param system_random: The randomizer used to generate secret_keys.
    :paramtype system_random: random.SystemRandom|None
    :returns: Randomized string, or if None system_random passed then "CHANGEME!!!"
    """
    if system_random is None:
        # This return CHANGEME, and when combined with the warning during
        # import encourages the cookiecutter user to come up with their
        # own random keys
        return 'CHANGEME!!!'

    return ''.join([system_random.choice(CHARS) for i in range(length)])
