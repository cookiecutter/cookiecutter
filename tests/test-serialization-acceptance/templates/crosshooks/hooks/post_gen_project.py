#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from cookiecutter.serialization import get_context


def create_file(name, content=''):
    file = os.path.join(os.getcwd(), name)
    open(file, 'w').write(content)


context = get_context()
create_file('crosshooks', context['for_post'])
