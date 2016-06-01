#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from cookiecutter.serialization import SerializationFacade

serializer = SerializationFacade()
context = serializer.deserialize(sys.stdin.readlines()[0])
context['inplace'] = os.path.realpath(__file__)
print(serializer.serialize(context))
