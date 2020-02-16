#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple post-gen hook for testing project folder and custom file creation."""

from __future__ import print_function

print('pre generation hook')
f = open('python_post.txt', 'w')
f.close()
