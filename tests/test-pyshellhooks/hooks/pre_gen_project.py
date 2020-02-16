#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple pre-gen hook for testing project folder and custom file creation."""

from __future__ import print_function

print('pre generation hook')
f = open('python_pre.txt', 'w')
f.close()
