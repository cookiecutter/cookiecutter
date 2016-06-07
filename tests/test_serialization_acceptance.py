#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_real_hooks_acceptance
--------------------------

Additional tests for `cookiecutter.hooks` module.
"""

import os

from .support import AbstractAcceptanceTest


class TestSerializationAcceptance(AbstractAcceptanceTest):

    def _repo_id(self):
        return 'test-serialization-acceptance'

    def test_cross_hooks_context(self):
        """
        context can be updated from a hook to another
        """
        template = 'crosshooks'
        self.run(template)
        assert os.path.exists(os.path.join(self.project_dir, template))

    def test_custom_serializer(self):
        """
        context can be updated from a hook to another
        """
        template = 'custom_serializer'
        self.run(template)
        assert os.path.exists(os.path.join(self.project_dir, 'COPY'))
