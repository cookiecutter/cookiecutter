"""Jinja2 extensions."""

from __future__ import annotations

import json
import string
import uuid
from secrets import choice
from typing import TYPE_CHECKING, Any, Iterable

import arrow
from jinja2 import Environment, nodes
from jinja2.ext import Extension
from slugify import slugify as pyslugify
from slugify.slugify import DEFAULT_SEPARATOR

if TYPE_CHECKING:
    import re

    from jinja2.parser import Parser


class JsonifyExtension(Extension):
    """Jinja2 extension to convert a Python object to JSON."""

    def __init__(self, environment: Environment) -> None:
        """Initialize the extension with the given environment."""
        super().__init__(environment)

        def jsonify(obj: Any, indent: int = 4) -> str:
            return json.dumps(obj, sort_keys=True, indent=indent)

        environment.filters['jsonify'] = jsonify


class RandomStringExtension(Extension):
    """Jinja2 extension to create a random string."""

    def __init__(self, environment: Environment) -> None:
        """Jinja2 Extension Constructor."""
        super().__init__(environment)

        def random_ascii_string(
            length: int, numbers: bool = False, punctuation: bool = False
        ) -> str:
            """Generate a random ASCII string.

            :param length: Length of the generated string.
            :param number: Whether to include digits.
            :param punctuation: Whether to include punctuation.
            :returns: Random ASCII string.
            """

            corpus = string.ascii_letters  # Start with letters

            if numbers:
                corpus += string.digits  # Add digits if requested
            if punctuation:
                corpus += string.punctuation  # Add punctuation if requested

            return "".join(choice(corpus) for _ in range(length))

        environment.globals.update(random_ascii_string=random_ascii_string)


class SlugifyExtension(Extension):
    """Jinja2 Extension to slugify string."""

    def __init__(self, environment: Environment) -> None:
        """Jinja2 Extension constructor."""
        super().__init__(environment)

        def slugify(
            value: str,
            entities: bool = True,
            decimal: bool = True,
            hexadecimal: bool = True,
            max_length: int = 0,
            word_boundary: bool = False,
            separator: str = DEFAULT_SEPARATOR,
            save_order: bool = False,
            stopwords: Iterable[str] = (),
            regex_pattern: re.Pattern[str] | str | None = None,
            lowercase: bool = True,
            replacements: Iterable[Iterable[str]] = (),
            allow_unicode: bool = False,
        ) -> str:
            """Slugifies the value."""
            return pyslugify(
                value,
                entities,
                decimal,
                hexadecimal,
                max_length,
                word_boundary,
                separator,
                save_order,
                stopwords,
                regex_pattern,
                lowercase,
                replacements,
                allow_unicode,
            )

        environment.filters['slugify'] = slugify


class UUIDExtension(Extension):
    """Jinja2 Extension to generate uuid4 string."""

    def __init__(self, environment: Environment) -> None:
        """Jinja2 Extension constructor."""
        super().__init__(environment)

        def uuid4() -> str:
            """Generate UUID4."""
            return str(uuid.uuid4())

        environment.globals.update(uuid4=uuid4)


class TimeExtension(Extension):
    """Jinja2 Extension for dates and times."""

    tags = {'now'}

    def __init__(self, environment: Environment) -> None:
        """Jinja2 Extension constructor."""
        super().__init__(environment)

        environment.extend(datetime_format='%Y-%m-%d')

    def _datetime(
        self,
        timezone: str,
        operator: str,
        offset: str,
        datetime_format: str | None,
    ) -> str:
        d = arrow.now(timezone)

        # parse shift params from offset and include operator
        shift_params = {}
        for param in offset.split(','):
            interval, value = param.split('=')
            shift_params[interval.strip()] = float(operator + value.strip())
        d = d.shift(**shift_params)

        if datetime_format is None:
            datetime_format = self.environment.datetime_format  # type: ignore[attr-defined]
        return d.strftime(datetime_format)

    def _now(self, timezone: str, datetime_format: str | None) -> str:
        if datetime_format is None:
            datetime_format = self.environment.datetime_format  # type: ignore[attr-defined]
        return arrow.now(timezone).strftime(datetime_format)

    def parse(self, parser: Parser) -> nodes.Output:
        """Parse datetime template and add datetime value."""
        lineno = next(parser.stream).lineno

        node = parser.parse_expression()

        if parser.stream.skip_if('comma'):
            datetime_format = parser.parse_expression()
        else:
            datetime_format = nodes.Const(None)

        if isinstance(node, nodes.Add):
            call_method = self.call_method(
                '_datetime',
                [node.left, nodes.Const('+'), node.right, datetime_format],
                lineno=lineno,
            )
        elif isinstance(node, nodes.Sub):
            call_method = self.call_method(
                '_datetime',
                [node.left, nodes.Const('-'), node.right, datetime_format],
                lineno=lineno,
            )
        else:
            call_method = self.call_method(
                '_now',
                [node, datetime_format],
                lineno=lineno,
            )
        return nodes.Output([call_method], lineno=lineno)
