
import os

_scripts_dir = os.path.dirname(os.path.realpath(__file__))


def _path(folder):
    return os.path.join(_scripts_dir, '..', folder)


_resourcesPath = _path('resources')
_cachePath = _path('cache')
_dataPath = _path('data')


def _file(path, filename, read, binary=False):
    mode = 'r' if read else 'w'
    flag = 'b' if binary else ''
    filepath = os.path.join(path, filename)
    if not read:
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
    return open(filepath, mode + flag)


def text(filename):
    with _file(_resourcesPath, filename, True) as file:
        return file.read()


def json(filename):
    import json
    return json.loads(text(filename))


def _load(path, filename):
    import pickle
    try:
        with _file(path, filename, True, True) as file:
            return True, pickle.load(file)
    except:
        return False, None


def _store(path, filename, data):
    import pickle
    with _file(_cachePath, filename, False, True) as file:
        pickle.dump(data, file)


def loadCache(filename):
    return _load(_cachePath, filename)


def storeCache(filename, data):
    return _store(_cachePath, filename, data)


def load(filename):
    return _load(_dataPath, filename)


def store(filename, data):
    return _store(_dataPath, filename, data)
