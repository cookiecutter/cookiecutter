import sys

PY3 = sys.version_info[0] == 3
OLD_PY2 = sys.version_info[:2] < (2, 7)


if PY3:  # pragma: no cover
    iteritems = lambda d: iter(d.items())


else:  # pragma: no cover
    iteritems = lambda d: d.iteritems()
