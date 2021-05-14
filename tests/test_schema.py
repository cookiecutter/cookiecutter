import json

import pytest
from jsonschema import ValidationError

from cookiecutter.schema import infer_schema_version, validate


def test_validate_1_0():
    d = get_sample_cookiecutter('1.0')
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


def test_validate_unsupported_version():
    d = get_sample_cookiecutter('2.0')
    with pytest.raises(ValueError):
        validate(d, version='2.175')


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
    with pytest.warns(UserWarning):
        validate(d)


def test_validate_fail_additions():
    d = get_sample_cookiecutter('2.0')
    d['addition'] = "yolo!"
    with pytest.raises(ValidationError):
        validate(d)


def test_validate_fail_additions_2():
    d = get_sample_cookiecutter('2.0')
    d['template']['descriptin'] = "oops, typo :/"
    with pytest.raises(ValidationError):
        validate(d)


def test_validate_fail_additions_3():
    d = get_sample_cookiecutter('2.0')
    d['template']['variables'][0]['addition'] = "yolo!"
    with pytest.raises(ValidationError):
        validate(d)


def test_detect_1_0():
    # testing a version 1 without version in it
    d = get_sample_cookiecutter('1.0.1')
    assert infer_schema_version(d) == '1.0'


def test_detect_2_0():
    d = get_sample_cookiecutter('2.0')
    assert infer_schema_version(d) == '2.0'


def test_infer_fallback_1_0():
    d = get_sample_cookiecutter('2.0')
    d['version'] = "2.42"
    with pytest.warns(UserWarning):
        assert infer_schema_version(d) == '1.0'


def get_sample_cookiecutter(version='2.0.0'):
    with open(f'tests/test-context/cookiecutter-{version}.json') as fp:
        return json.load(fp)
