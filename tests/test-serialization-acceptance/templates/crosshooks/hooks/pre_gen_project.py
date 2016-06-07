#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cookiecutter.serialization import get_context, put_context


context = get_context()

context['for_post'] = 'From pre_gen_project to post_gen_project'

put_context(context)
