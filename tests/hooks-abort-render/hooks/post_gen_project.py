# flake8: noqa

"""Simple post-gen hook for testing the handling of different exit codes."""

import sys

{% if cookiecutter.abort_post_gen == "yes" %}
sys.exit(5)
{% else %}
sys.exit(0)
{% endif %}
