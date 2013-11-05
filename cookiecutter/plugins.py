import logging
import pkg_resources
from jinja2 import nodes
from jinja2.ext import Extension

logger = logging.getLogger(__name__)


class JinjaSimpleTag(Extension):
    def parse(self, parser):

        lineno = parser.stream.next().lineno
        args = [parser.parse_expression()]

        # Why return a CallBlock when we have no body?
        #
        # http://stackoverflow.com/questions/5972458/help-with-custom-jinja2-extension
        # The reason is that parse() is expected to return a statement node,
        # such as CallBlock or Assign. call_method() returns an expression
        # node, which you must wrap in CallBlock to have a statement.
        return nodes.CallBlock(self.call_method('tag_action', args),
                               [], [], []).set_lineno(lineno)

    def tag_action(self, data, caller):
        '''
        Override point for users
        '''
        return ''


def plugins_for_namespace(namespace):
    entry_points = list(pkg_resources.iter_entry_points(namespace))
    return entry_points


def load_jinja_plugins():
    entry_points = plugins_for_namespace('cookiecutter.plugins.jinja')
    return [x.load() for x in entry_points]
