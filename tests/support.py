#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
support
-------

Add test support utilities which are globally available throughout the suite.
"""

from cookiecutter.main import cookiecutter


class Runner(object):
    """
    helper class to run cookierunner main command
    """

    def __init__(self, settings):
        """
        :param settings: SettingObject instance
        """
        self.settings = settings

    def run(self):
        """
        run cookiecutter
        """
        cookiecutter(
            self.settings.template,
            self.settings.checkout,
            self.settings.no_input,
            self.settings.extra_context,
            self.settings.replay,
            self.settings.overwrite_if_exists,
            self.settings.output_dir,
            self.settings.config_file
        )


class SettingObject(object):
    """
    config object to pass to the runner instance to configure the cookiecutter
    runtime environment
    """

    def __init__(
        self, template_dir, config_file,
        extra_context=None, output_dir=u'.'
    ):
        """
        :param template_dir: the template directory
        :param config_file: path to the user cookiecutterrc file
        :param extra_context: extra context dictionary
        :output_dir: output directory
        """
        self.template = template_dir
        self.checkout = None
        self.no_input = True
        self.extra_context = extra_context
        self.replay = False
        self.overwrite_if_exists = False
        self.output_dir = output_dir
        self.config_file = config_file
