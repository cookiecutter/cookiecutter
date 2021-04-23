import json

from cookiecutter.schema import validate


def test_validate():
    with open('tests/test-context/cookiecutter-2.0.json') as fp:
        d = json.load(fp)
        validate(d)
    pass
