#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

hooks_dir = os.path.dirname(__file__)
sys.path.append(hooks_dir)

from support import create_file

template_dir = os.path.dirname(hooks_dir)
create_file('inplace', template_dir)
