import os
import sys

PY3 = sys.version_info[0] == 3
OLD_PY2 = sys.version_info[:2] < (2, 7)

if PY3:  # pragma: no cover
    input_str = 'builtins.input'
    iteritems = lambda d: iter(d.items())
    from unittest.mock import patch
    from io import StringIO

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


if PY3:  # Forced testing

    from shutil import which

else:  # Forced testing

    def is_exe(program):
        """
        Returns whether or not a file is an executable.
        """
        return os.path.isfile(program) and os.access(program, os.X_OK)

    def which(cmd, mode=os.F_OK | os.X_OK, path=None):
        """Given a command, mode, and a PATH string, return the path which
        conforms to the given mode on the PATH, or None if there is no such
        file.
        `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
        of os.environ.get("PATH"), or can be overridden with a custom search
        path.

        Note: This function was backported from the Python 3 source code.
        """
        # Check that a given file can be accessed with the correct mode.
        # Additionally check that `file` is not a directory, as on Windows
        # directories pass the os.access check.
        def _access_check(fn, mode):
            return (os.path.exists(fn) and os.access(fn, mode)
                    and not os.path.isdir(fn))

        # If we're given a path with a directory part, look it up directly
        # rather than referring to PATH directories. This includes checking
        # relative to the current directory, e.g. ./script
        if os.path.dirname(cmd):
            if _access_check(cmd, mode):
                return cmd
            return None

        if path is None:
            path = os.environ.get("PATH", os.defpath)
        if not path:
            return None
        path = path.split(os.pathsep)

        if sys.platform == "win32":
            # The current directory takes precedence on Windows.
            if os.curdir not in path:
                path.insert(0, os.curdir)

            # PATHEXT is necessary to check on Windows.
            pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
            # See if the given file matches any of the expected path
            # extensions. This will allow us to short circuit when given
            # "python.exe". If it does match, only test that one, otherwise we
            # have to try others.
            if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
                files = [cmd]
            else:
                files = [cmd + ext for ext in pathext]
        else:
            # On other platforms you don't have things like PATHEXT to tell you
            # what file suffixes are executable, so just pass on cmd as-is.
            files = [cmd]

        seen = set()
        for dir in path:
            normdir = os.path.normcase(dir)
            if normdir not in seen:
                seen.add(normdir)
                for thefile in files:
                    name = os.path.join(dir, thefile)
                    if _access_check(name, mode):
                        return name
        return None


def is_string(obj):
    """Determine if an object is a string."""
    return isinstance(obj, str if PY3 else basestring)


_hush_pyflakes = (patch, StringIO, which)
