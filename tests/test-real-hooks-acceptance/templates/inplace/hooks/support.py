#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def create_file(name, content=''):
    file = os.path.join(os.getcwd(), name)
    open(file, 'w').write(content)
