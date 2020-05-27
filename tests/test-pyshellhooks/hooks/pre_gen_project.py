#!/usr/bin/env python
"""Simple pre-gen hook for testing project folder and custom file creation."""


print('pre generation hook')
f = open('python_pre.txt', 'w')
f.close()
