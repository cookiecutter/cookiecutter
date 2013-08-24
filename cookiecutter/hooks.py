#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.hooks
------------------

Functions for discovering and executing various cookiecutter hooks.
"""

import os
import subprocess

_HOOKS = {
    'pre_gen_project': None,
    'post_gen_project': None,
    # TODO: other hooks should be listed here
}

def find_hooks(template_root):
    ''' '''
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
    ''' '''
    subprocess.call(script_path, cwd=cwd)

def run_hook(hook_name, input_dir output_dir):
    ''' '''
    pass
