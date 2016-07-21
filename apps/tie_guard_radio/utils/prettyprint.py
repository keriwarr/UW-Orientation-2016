import json


def prettyprint(data):
    print json.dumps(data, sort_keys=True,
        indent=4, separators=(',', ': '))
