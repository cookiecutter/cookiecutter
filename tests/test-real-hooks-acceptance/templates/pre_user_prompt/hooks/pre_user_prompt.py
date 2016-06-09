#!/usr/bin/env python
# -*- coding: utf-8 -*-

import helpers

from cookiecutter.serialization import get_context, put_context
from cookiecutter.config import set_to_cookiecutter_context


context = get_context()
set_to_cookiecutter_context(context, 'license', helpers.get_licenses())
put_context(context)
