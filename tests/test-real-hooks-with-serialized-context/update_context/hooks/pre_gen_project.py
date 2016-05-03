#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json

print("Dummy message")

context = json.loads(sys.stdin.readlines()[0])
context['my_key'] = 'not_kept_as_not_last_val'
print(json.dumps(context))

context['my_key'] = 'my_val_updated'
print(json.dumps(context))

print("Dummy message")
