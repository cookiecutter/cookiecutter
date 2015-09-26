# -*- coding: utf-8 -*-

import locale
import codecs
import pytest
import sys

PY3 = sys.version_info[0] == 3


@pytest.mark.skipif(not PY3, reason='Only necessary on Python3')
def test_not_ascii():
    """Make sure that the systems preferred encoding is not `ascii`.

    Otherwise `click` is raising a RuntimeError for Python3. For a detailed
    description of this very problem please consult the following gist:
    https://gist.github.com/hackebrot/937245251887197ef542

    This test also checks that `tox.ini` explicitly copies the according
    system environment variables to the test environments.
    """
    try:
        preferred_encoding = locale.getpreferredencoding()
        fs_enc = codecs.lookup(preferred_encoding).name
    except Exception:
        fs_enc = 'ascii'
    assert fs_enc != 'ascii'
