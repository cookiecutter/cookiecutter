#!/usr/bin/env python
"""Simple post-gen hook for testing project folder and custom file creation."""

print('pre generation hook')
f = open('python_post.txt', 'w')
f.close()
