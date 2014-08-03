import sys
import platform

PY3 = sys.version > '3'
PY_VERSION = sys.version_info[:3]
WINDOWS = 'windows' in platform.system().lower()

if PY3:
    iteritems = lambda d: iter(d.items())
    from io import StringIO, open
    import json
    from collections import OrderedDict

    import unittest
    from unittest.mock import patch
    input_str = 'builtins.input'
else:
    import __builtin__
    iteritems = lambda d: d.iteritems()
    from codecs import open as open

    from mock import patch
    input_str = '__builtin__.raw_input'
    input = raw_input
    from cStringIO import StringIO

    if PY_VERSION < (2, 7):
        import simplejson as json
        from ordereddict import OrderedDict
        import unittest2 as unittest
    else:
        import json
        from collections import OrderedDict
        import unittest
