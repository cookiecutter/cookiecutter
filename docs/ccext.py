# -*- coding: utf-8 -*-
import sys
from cookiecutter import main
from docutils import nodes
from docutils.parsers import rst
from docutils.statemachine import ViewList


class CcCommandLineOptions(rst.Directive):
    def _format_action(self, action):
        bookmark_line = ".. _`%s`:" % action.dest
        line = ".. option:: "
        line += ", ".join(action.option_strings)
        opt_help = action.help.replace('%default', str(action.default))

        # fix paths with sys.prefix
        opt_help = opt_help.replace(sys.prefix, "<sys.prefix>")

        return [bookmark_line, "", line, "", " %s" % opt_help, ""]

    def process_actions(self):
        parser = main._get_parser()
        for action in parser._actions:
            if not action.option_strings:
                continue
            for line in self._format_action(action):
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
