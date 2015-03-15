#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_vcs_prompt
---------------
"""

import os
import pytest

from cookiecutter import utils


@pytest.fixture
def clean_cookiecutter_dirs(request):
    if os.path.isdir('cookiecutter-pypackage'):
        utils.rmtree('cookiecutter-pypackage')
    os.mkdir('cookiecutter-pypackage/')
    if os.path.isdir('cookiecutter-trytonmodule'):
        utils.rmtree('cookiecutter-trytonmodule')
    os.mkdir('cookiecutter-trytonmodule/')

    def remove_cookiecutter_dirs():
        if os.path.isdir('cookiecutter-pypackage'):
            utils.rmtree('cookiecutter-pypackage')
        if os.path.isdir('cookiecutter-trytonmodule'):
            utils.rmtree('cookiecutter-trytonmodule')
    request.addfinalizer(remove_cookiecutter_dirs)
