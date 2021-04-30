import json

from cookiecutter.schema import validate


def test_validate_1_0_0():
    with open('tests/test-context/cookiecutter-1.0.0.json') as fp:
        d = json.load(fp)
        validate(d, version='1.0.0')


def test_validate_2_0_0():
    with open('tests/test-context/cookiecutter-2.0.0.json') as fp:
        d = json.load(fp)
        validate(d, version='2.0.0')
