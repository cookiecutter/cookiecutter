#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from support import create_file

hooks_dir = os.path.dirname(__file__)
sys.path.append(hooks_dir)


template_dir = os.path.dirname(hooks_dir)
create_file('inplace', template_dir)
