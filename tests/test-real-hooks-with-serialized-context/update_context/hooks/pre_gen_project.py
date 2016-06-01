#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from cookiecutter.serialization import SerializationFacade

print("Dummy message")

serializer = SerializationFacade()
context = serializer.deserialize(sys.stdin.readlines()[0])
context['my_key'] = 'not_kept_as_not_last_val'
print(serializer.serialize(context))

context['my_key'] = 'my_val_updated'
print(serializer.serialize(context))

print("Dummy message")
