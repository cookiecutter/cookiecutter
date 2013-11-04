#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.hooks
------------------

Functions for discovering and executing various cookiecutter hooks.
"""

import logging
import os
import stat
import subprocess
import sys
import tempfile

from jinja2 import Template

from .utils import make_sure_path_exists, unicode_open, work_in

_HOOKS = [
    'pre_gen_project',
    'post_gen_project',
    # TODO: other hooks should be listed here
]

def find_hooks():
    '''
    Must be called with the project template as the current working directory.
    Returns a dict of all hook scripts provided.
    Dict's key will be the hook/script's name, without extension, while
    values will be the absolute path to the script.
    Missing scripts will not be included in the returned dict.
    '''
    hooks_dir = 'hooks'
    r = {}
    logging.debug("hooks_dir is {0}".format(hooks_dir))
    if not os.path.isdir(hooks_dir):
        logging.debug("No hooks/ dir in template_dir")
        return r
    for f in os.listdir(hooks_dir):
        basename = os.path.splitext(os.path.basename(f))[0]
        if basename in _HOOKS:
            r[basename] = os.path.abspath(os.path.join(hooks_dir, f))
    return r


def _run_hook(script_path, cwd='.', context={}):
    '''
    Run a sigle external script located at `script_path` (path should be
    absolute).
    If `cwd` is provided, the script will be run from that directory.
    script is first run through jinja template and context passed
    '''
    with open(script_path, 'r') as f:
        content = f.read()
    outfile_tmpl = Template(content)
    output = outfile_tmpl.render(**context)
    
    fd, temp_script_path = tempfile.mkstemp()
    os.write(fd, output)
    
    st = os.stat(temp_script_path)
    os.chmod(temp_script_path, st.st_mode | stat.S_IEXEC)

    run_thru_shell = sys.platform.startswith('win')
    proc = subprocess.Popen(
        script_path,
        shell=run_thru_shell,
        cwd=cwd
    )
    proc.wait()
    os.close(fd)

def run_hook(hook_name, project_dir, context={}):
    '''
    Try and find a script mapped to `hook_name` in the current working directory,
    and execute it from `project_dir`.
    '''
    script = find_hooks().get(hook_name)
    if script is None:
        logging.debug("No hooks found")
        return
    return _run_hook(script, project_dir)
