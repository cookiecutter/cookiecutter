"""Jinja2 extensions."""
import json
import string
from secrets import choice

from jinja2.ext import Extension
from slugify import slugify as pyslugify


class JsonifyExtension(Extension):
    """Jinja2 extension to convert a Python object to JSON."""

    def __init__(self, environment):
        """Initialize the extension with the given environment."""
        super(JsonifyExtension, self).__init__(environment)

        def jsonify(obj):
            return json.dumps(obj, sort_keys=True, indent=4)

        environment.filters['jsonify'] = jsonify


class RandomStringExtension(Extension):
    """Jinja2 extension to create a random string."""

    def __init__(self, environment):
        """Jinja2 Extension Constructor."""
        super(RandomStringExtension, self).__init__(environment)

        def random_ascii_string(length, punctuation=False):
            if punctuation:
                corpus = "".join((string.ascii_letters, string.punctuation))
            else:
                corpus = string.ascii_letters
            return "".join(choice(corpus) for _ in range(length))

        environment.globals.update(random_ascii_string=random_ascii_string)


class SlugifyExtension(Extension):
    """Jinja2 Extension to slugify string."""

    def __init__(self, environment):
        """Jinja2 Extension constructor."""
        super(SlugifyExtension, self).__init__(environment)

        def slugify(value, **kwargs):
            """Slugifies the value."""
            return pyslugify(value, **kwargs)

        environment.filters['slugify'] = slugify
