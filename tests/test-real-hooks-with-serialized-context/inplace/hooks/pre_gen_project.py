#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import os

context = json.loads(sys.stdin.readlines()[0])
context['inplace'] = os.path.realpath(__file__)
print(json.dumps(context))
