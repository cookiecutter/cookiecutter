#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

{% if cookiecutter.abort_post_gen == "yes" %}
sys.exit(1)
{% else %}
sys.exit(0)
{% endif %}
