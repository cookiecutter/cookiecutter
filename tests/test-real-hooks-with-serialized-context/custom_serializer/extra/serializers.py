import os

from cookiecutter.serialization import JsonSerializer


class CustomSerializer(JsonSerializer):

    def _do_serialize(self, subject):
        subject['template_dir'] = os.path.dirname(os.path.dirname(__file__))

        return super(CustomSerializer, self)._do_serialize(subject)
