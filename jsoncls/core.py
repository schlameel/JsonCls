'''Supporting functionality

Created on Apr 2, 2013

@author: schlameel
@copyright: Schlameel
@license: GPL v3.0
'''

import json

class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__reprJSON__'):
            return obj.__reprJSON__()
        else:
            try:
                s = json.JSONEncoder.default(self, obj)
                return s
            except TypeError as e:
                #print obj
                # Removing print statement for initial python3 testing
                pass

def json_dumps(obj, indent=0):
    if indent:
        return json.dumps(obj, cls=ObjectEncoder, indent=indent)
    else:
        return json.dumps(obj, cls=ObjectEncoder)
