import logging
import pkg_resources
from jinja2 import nodes
from jinja2.ext import Extension

logger = logging.getLogger(__name__)


class JinjaSimpleTag(Extension):
    def __init__(self, environment):
        super(JinjaSimpleTag, self).__init__(environment)

    def parse(self, parser):

        lineno = parser.stream.next().lineno

        # Why return a CallBlock when we have no body?
        #
        # http://stackoverflow.com/questions/5972458/help-with-custom-jinja2-extension
        # The reason is that parse() is expected to return a statement node,
        # such as CallBlock or Assign. call_method() returns an expression
        # node, which you must wrap in CallBlock to have a statement.
        return nodes.CallBlock(self.call_method('tag_action', None),
                               [], [], []).set_lineno(lineno)

    def tag_action(self, caller):
        '''
        Override point for users
        '''
        return ''


def plugins_for_namespace(namespace):
    entry_points = list(pkg_resources.iter_entry_points(namespace))
    return entry_points


def load_jinja_plugins():
    entry_points = plugins_for_namespace('cookiecutter.plugins.jinja')
    results = []

    for x in entry_points:
        try:
            results.append(x.load())
            logger.debug('Loaded Jinja plugin %s.%s', x.module_name, x.attrs[0])
        except ImportError:
            logger.error('Failed to load Jinja plugin %s.%s', x.module_name, x.attrs[0])
            pass

    return results
