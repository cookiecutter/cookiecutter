import json

import pytest
from jsonschema import ValidationError

from cookiecutter.schema import detect, validate


def test_validate_1_0():
    d = get_sample_cookiecutter('1.0')
    validate(d, version='1.0')


def test_validate_fail_1_0():
    d = get_sample_cookiecutter('1.0')
    d['my_dict'] = {'dicts': 'are not supported'}
    with pytest.raises(ValidationError):
        validate(d, version='1.0')


def test_validate_1_0_implicitly():
    d = get_sample_cookiecutter('1.0')
    validate(d)


def test_validate_1_0_fallback():
    d = get_sample_cookiecutter('1.0')
    del d['version']
    validate(d)


def test_validate_2_0():
    d = get_sample_cookiecutter('2.0')
    validate(d, version='2.0')


def test_validate_fail_2_0():
    d = get_sample_cookiecutter('2.0')
    d['authors'] = "authors must be an array"
    with pytest.raises(ValidationError):
        validate(d, version='2.0')


def test_validate_2_0_implicitly():
    d = get_sample_cookiecutter('2.0')
    validate(d)


def test_validate_fail_unsupported():
    d = get_sample_cookiecutter('2.0')
    d['version'] = "2.42"
    with pytest.raises(ValueError):
        validate(d)


def test_detect_1_0():
    # testing a version 1 withou version in it
    d = get_sample_cookiecutter('1.0.1')
    assert detect(d) == '1.0'


def test_detect_2_0():
    d = get_sample_cookiecutter('2.0')
    assert detect(d) == '2.0'


def test_detect_invalid():
    d = get_sample_cookiecutter('2.0')
    d['version'] = "2.42"
    assert detect(d) is None


def get_sample_cookiecutter(version='2.0.0'):
    with open(f'tests/test-context/cookiecutter-{version}.json') as fp:
        return json.load(fp)
