#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_generate_files
-------------------

Test formerly known from a unittest residing in test_generate.py named
TestGenerateFiles.test_generate_files_nontemplated_exception
"""

import pytest
from cookiecutter import generate
from cookiecutter import exceptions


@pytest.mark.usefixtures("clean_system")
def test_generate_files_nontemplated_exception():
    with pytest.raises(exceptions.NonTemplatedInputDirException):
        generate.generate_files(
            context={'cookiecutter': {'food': 'pizza'}},
            repo_dir='tests/test-generate-files-nontemplated'
        )
