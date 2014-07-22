import sys
import platform

PY3 = sys.version > '3'
WINDOWS = 'windows' in platform.system().lower()

if PY3:
    from unittest.mock import patch
    input_str = 'builtins.input'
    iteritems = lambda d: iter(d.items())
else:
    import __builtin__
    from mock import patch
    input_str = '__builtin__.raw_input'
    from cStringIO import StringIO
    input = raw_input
    iteritems = lambda d: d.iteritems()
    from codecs import open as open

    if sys.version_info[:3] < (2, 7):
        import unittest2 as unittest
    else:
        import unittest
