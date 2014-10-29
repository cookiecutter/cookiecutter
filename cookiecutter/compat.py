import sys

PY3 = sys.version_info[0] == 3
OLD_PY2 = sys.version_info[:2] < (2, 7)

if PY3:  # pragma: no cover
    input_str = 'builtins.input'
    iteritems = lambda d: iter(d.items())
    from unittest.mock import patch
    from io import StringIO
    import unittest

    import json
    from collections import OrderedDict

    def read_response(prompt=''):
        """
        Prompt the user for a response.

        Prints the given prompt (which should be a Unicode string),
        and returns the text entered by the user as a Unicode string.

        :param prompt: A Unicode string that is presented to the user.
        """
        # The Python 3 input function does exactly what we want
        return input(prompt)
else:  # pragma: no cover
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

    def read_response(prompt=''):
        """
        Prompt the user for a response.

        Prints the given prompt (which should be a Unicode string),
        and returns the text entered by the user as a Unicode string.

        :param prompt: A Unicode string that is presented to the user.
        """
        # For Python 2, raw_input takes a byte string argument for the prompt.
        # This must be encoded using the encoding used by sys.stdout.
        # The result is a byte string encoding using sys.stdin.encoding.
        # However, if the program is not being run interactively, sys.stdout
        # and sys.stdin may not have encoding attributes.
        # In that case we don't print a prompt (stdin/out isn't interactive,
        # so prompting is pointless), and we assume the returned data is
        # encoded using sys.getdefaultencoding(). This may not be right,
        # but it's likely the best we can do.
        # Isn't Python 2 encoding support wonderful? :-)
        if sys.stdout.encoding:
            prompt = prompt.encode(sys.stdout.encoding)
        else:
            prompt = ''
        enc = sys.stdin.encoding or sys.getdefaultencoding()
        return raw_input(prompt).decode(enc)

_hush_pyflakes = (patch, StringIO, json, OrderedDict, unittest)
