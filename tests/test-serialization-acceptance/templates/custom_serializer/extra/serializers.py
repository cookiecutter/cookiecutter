import os

from cookiecutter.serialization import JsonSerializer


class CustomSerializer(JsonSerializer):

    def _do_serialize(self, subject):
        subject['resources'] = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'resources'
        )

        return super(CustomSerializer, self)._do_serialize(subject)
