#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.config
-------------------

Global configuration handling
"""

import logging
import os
import sys

if sys.version_info[:2] < (2, 7):
    import simplejson as json
    from ordereddict import OrderedDict
else:
    import json
    from collections import OrderedDict

from .utils import unicode_open



def _json_parse(json_string, comment_char='#', *args, **kwargs):
	"""
	Remove any line begining with `comment_char` from `json_string`,
	and return a json object from it.
	*args & **kwargs will be passed to json.loads.
	"""
	lines = json_string.split('\n')
	for l in lines:
		if l.strip().startswith(comment_char):
			logging.debug("Ignoring config comment: %s" % l)
			lines.remove(l)
	return json.loads(''.join(lines), *args, **kwargs)

def _json_open(json_path, *args, **kwargs):
	"""
	Open a json file containing comments (see _json_parse).
	"""
	with unicode_open(json_path) as fh:
		obj = _json_parse(fh.read(), *args, **kwargs)
	return obj