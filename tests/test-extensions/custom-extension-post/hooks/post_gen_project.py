# -*- coding: utf-8 -*-

# flake8: noqa

"""Sample post-gen hook for testing that custom extensions are available and exposed methods are callable."""
import sys

if '{% hello cookiecutter.name %}' == 'Hello Cookiemonster!':
    sys.exit(0)
else:
    sys.exit(1)
