import json
from json import JSONEncoder

class HouseEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__
