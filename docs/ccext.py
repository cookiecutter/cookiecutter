# -*- coding: utf-8 -*-

"""Custom Sphinx extension to build a list of all of cookiecutter's cli."""

import click
from docutils import nodes
from docutils.parsers import rst
from docutils.statemachine import ViewList

from cookiecutter import cli


class CcCommandLineOptions(rst.Directive):
    """Custom docutils extension class to parse cli commands from code."""

    def _format_option(self, option):
        """Do cli options formatting."""
        return [
            ".. _`%s`:" % option.name,
            "",
            ".. option:: " + ", ".join(option.opts),
            "",
            option.help,
            ""
        ]

    def process_actions(self):
        """Get options from cookiecutter, send to formatter, prepare result."""
        for option in cli.main.params:
            if isinstance(option, click.core.Option):
                for line in self._format_option(option):
                    self.view_list.append(line, "")

    def run(self):
        """Override `run` in `rst.Directive` class."""
        node = nodes.paragraph()
        node.document = self.state.document
        self.view_list = ViewList()
        self.process_actions()
        self.state.nested_parse(self.view_list, 0, node)
        return [node]


def setup(app):
    """Register a Docutils extension directive."""
    app.add_directive('cc-command-line-options', CcCommandLineOptions)
