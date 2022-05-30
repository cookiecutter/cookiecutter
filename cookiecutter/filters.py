"""Jinja2 custom filters and functions loading."""

import glob
import importlib
import os
import pathlib
import sys


def import_py_files(module_dir):
    """
    Import python files from template repo dir.
    """
    if not os.path.exists(module_dir):
        return

    sys.path.append(module_dir)
    py_files = glob.glob(os.path.join(module_dir, '*.py'))

    for py_file in py_files:
        module_name = pathlib.Path(py_file).stem
        importlib.import_module(module_name)


def load_custom_filters(repo_dir, context, env):
    """
    Load custom filters for jinja2
    :param repo_dir: Project template input directory.
    :param context: Cookiecutter project context.
    :param env: Strict Jinja2 environment
    :return:
    """
    filters = context['cookiecutter'].get("_filters")
    if not filters:
        return

    module_dir = f'{repo_dir}/filters'
    import_py_files(module_dir)

    for key, value in filters.items():
        model = importlib.import_module("filter")
        try:
            func = getattr(model, value)
            env.filters[key] = func
        except AttributeError:
            pass
