from sys import version_info


PY3 = version_info[0] == 3
OLD_PY2 = version_info[:2] < (2, 7)

if PY3:
    input_str = 'builtins.input'
    iteritems = lambda d: iter(d.items())
    from unittest.mock import patch
    from io import StringIO
    import unittest

    import json
    from collections import OrderedDict
else:
    from __builtin__ import raw_input
    input = raw_input
    input_str = '__builtin__.raw_input'
    iteritems = lambda d: d.iteritems()
    from mock import patch
    from cStringIO import StringIO

    if OLD_PY2:
        from ordereddict import OrderedDict
        import simplejson as json
        import unittest2 as unittest
    else:
        import json
        from collections import OrderedDict
        import unittest

_hush_pyflakes = (patch, StringIO, json, OrderedDict, unittest)
