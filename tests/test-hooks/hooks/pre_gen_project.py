#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os

print('pre generation hook')
f = open('python_pre.txt', 'w')
f.write(os.environ['test'])
f.close()

