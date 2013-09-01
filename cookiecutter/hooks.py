#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.hooks
------------------

Functions for discovering and executing various cookiecutter hooks.
"""

import os
import subprocess

_HOOKS = [
    'pre_gen_project',
    'post_gen_project',
    # TODO: other hooks should be listed here
]

def find_hooks(template_root):
    '''
    Return a dict of all hook scripts provided with the template located at
    `template_root`.
    Dict's key will be the hook/script's name, without extension, while
    values will be the absolute path to the script.
    Missing scripts will not be included in the returned dict.
    '''
    hooks_dir = os.path.join(template_root, 'hooks')
    r = {}
    if not os.path.isdir(hooks_dir):
        return r
    for f in os.listdir(hooks_dir):
        basename = os.path.splitext(os.path.basename(f))[0]
        if basename in _HOOKS:
            r[basename] = os.path.abspath(os.path.join(hooks_dir, f))
    return r


def _run_hook(script_path, cwd='.'):
    '''
    Run a sigle external script located at `script_path` (path should be 
    absolute).
    If `cwd` is provided, the script will be run from that directory.
    '''
    subprocess.call(script_path)


def run_hook(hook_name, input_dir, output_dir):
    '''
    Try and find a script mapped to `hook_name` in `input_dir`,
    and execute it with the current working directory.
    '''
    script = find_hooks(input_dir).get(hook_name)
    if script is None: 
        return
    return _run_hook(script, output_dir)
