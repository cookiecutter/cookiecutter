import os
import json


class CustomSerializer(object):

    def serialize(self, subject):
        subject['template_dir'] = os.path.dirname(os.path.dirname(__file__))
        return json.dumps(subject)

    def deserialize(self, string):
        return json.loads(string)
