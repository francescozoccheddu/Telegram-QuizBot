
import os

_scripts_dir = os.path.dirname(os.path.realpath(__file__))
_resourcesPath = os.path.join(_scripts_dir, '..', 'resources')


def text(filename):
    with open(os.path.join(_resourcesPath, filename), 'r') as file:
        return file.read()

def json(filename):
    import json
    return json.loads(text(filename))