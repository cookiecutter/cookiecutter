#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_serializers
----------------

Tests for `cookiecutter.serialization` serializer classes.
"""

from __future__ import unicode_literals

import pytest

from cookiecutter.serialization import JsonSerializer


@pytest.fixture
def get_serializers():
    """
    serializer provider
    """
    return {
        JsonSerializer: {"key": "value"}
    }


class TestSerialization(object):

    def test_serialize_return_type(self):
        """
        The serialize method should return a bytes string
        """
        serializers = get_serializers()
        for kclass in serializers:
            assert type(kclass().serialize(serializers[kclass])) == bytes

    def test_deserialize(self):
        """
        The deserialize method should return the previous object
        """
        serializers = get_serializers()
        for kclass in serializers:
            serializer = kclass()
            obj = serializers[kclass]
            string = serializer.serialize(obj)
            assert obj == serializer.deserialize(string)
