#!/usr/bin/env python
# flake8: noqa

"""Simple pre-gen hook for testing the handling of different exit codes."""

import sys

{% if cookiecutter.abort_pre_gen == "yes" %}
sys.exit(5)
{% else %}
sys.exit(0)
{% endif %}
