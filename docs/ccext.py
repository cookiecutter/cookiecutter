# -*- coding: utf-8 -*-
from cookiecutter import cli

import click

from docutils import nodes
from docutils.parsers import rst
from docutils.statemachine import ViewList


class CcCommandLineOptions(rst.Directive):
    def _format_option(self, option):
        return [
            ".. _`%s`:" % option.name,
            "",
            ".. option:: " + ", ".join(option.opts),
            "",
            option.help,
            ""
        ]

    def process_actions(self):
        for option in cli.main.params:
            if isinstance(option, click.core.Option):
                for line in self._format_option(option):
                    self.view_list.append(line, "")

    def run(self):
        node = nodes.paragraph()
        node.document = self.state.document
        self.view_list = ViewList()
        self.process_actions()
        self.state.nested_parse(self.view_list, 0, node)
        return [node]


def setup(app):
    app.add_directive('cc-command-line-options', CcCommandLineOptions)
