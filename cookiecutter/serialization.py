# -*- coding: utf-8 -*-
import json
import inspect
import re

from cookiecutter.utils import ApiChecker
from cookiecutter.exceptions import \
    UnknownSerializerType, BadSerializedStringFormat, InvalidSerializerType


class JsonSerializer(object):
    """
    The JSON serializer is the default serializer registered by the
    serialization facade
    It can serve as an example of the API that must implement custom
    serializers
    """

    def serialize(self, subject):
        """
        serialize a given subject to its JSON representation
        :param subject: the subject to serialize
        """
        return json.dumps(subject)

    def deserialize(self, string):
        """
        deserialize a given JSON string to its Python object
        :param string: the string to deserialize
        """
        return json.loads(string)


class SerializationFacade(object):
    """
    The SerializationFacade is the public API that customers should use.
    """

    def __init__(self, serializers=None):
        self.__serializers = {}
        self.__current_type = 'json'
        self.register('json', JsonSerializer)

        if serializers is not None:
            for type in serializers:
                self.register(type, serializers[type])

    def serialize(self, subject, type='json'):
        """
        serialize a given subject using a specific type (JSON by default)
        :param subject: the subject to serialize
        :param type: the serializer type to use
        """
        return type + '|' \
                    + self.__get_serializer(type).serialize(subject) \
                    + '$'

    def deserialize(self, string):
        """
        deserialize a given string which must be of the form:
        serializer_type|serialized_object
        :param string: the string to deserialize
        """
        parts = self.__get_last_serialized_part(string).split('|')

        if len(parts) < 2:
            raise BadSerializedStringFormat(
                message='Serialized string should be of the form '
                'serializer_type|serialized_string$'
            )

        return self.__get_serializer(parts[0]).deserialize(parts[1])

    def get_type(self):
        """
        get the type of the current serializer
        """
        return self.__current_type

    def register(self, type, serializer):
        """
        register a custom serializer
        :param type: type of the serializer to register
        :param serializer: custom serializer to register
        """
        self.__check_type(type)
        self.__check_serializer_api(serializer)
        self.__serializers[type] = serializer() if inspect.isclass(
            serializer) else serializer

    def __get_type_pattern(self):
        """
        get the validation pattern for serializer types
        """
        return '[a-zA-Z_][a-zA-Z_][a-zA-Z_0-9\-\.]+'

    def __get_serializer(self, type):
        """
        get the serializer of a given type
        :param type: type of the target serializer
        """
        if type in self.__serializers:
            self.__current_type = type
            return self.__serializers[type]

        else:
            raise UnknownSerializerType(type)

    def __check_serializer_api(self, serializer):
        """
        ensure that a given serializer implements the expected API
        :param serializer: serializer to check its public interface
        """
        ApiChecker('serialize', 'deserialize').implements_api(serializer)

    def __check_type(self, type):
        """
        ensure a given type is well formed and does not contain invalid chars
        :param type: the type to check
        """
        pattern = '^' + self.__get_type_pattern() + '$'
        if not re.match(pattern, type):
            raise InvalidSerializerType()

    def __get_last_serialized_part(self, string):
        """
        extract the last serialized part found in a mixed string
        """
        pattern = self.__get_type_pattern() + '\|[^\$]+'
        print(pattern)
        serialized_parts = re.findall(pattern, string)

        return serialized_parts[-1] if serialized_parts else string
