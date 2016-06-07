#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from cookiecutter.serialization import get_context
from shutil import copyfile


context = get_context()
src = os.path.join(
    context['resources'],
    'COPY'
)

dest = os.path.join(
    os.getcwd(),
    'COPY'
)

copyfile(src, dest)
