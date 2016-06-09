#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import helpers

from cookiecutter.serialization import get_context
from cookiecutter.config import get_from_cookiecutter_context


context = get_context()
license = get_from_cookiecutter_context(context, 'license')
src = helpers.get_license(license)
dest = os.path.join(os.getcwd(), license)

shutil.copyfile(src, dest)
