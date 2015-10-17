#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from cookiecutter.hooks import setup_virtualenv

print('pre generation hook')
f = open('python_post.txt', 'w')
f.close()
setup_virtualenv('./venv')
