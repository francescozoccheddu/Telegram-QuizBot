import os
import appdirs
from . import resources

_appInfo = resources.json('app.json')
_cachePath = appdirs.user_cache_dir(_appInfo['name'], _appInfo['author'])
_dataPath = appdirs.user_data_dir(_appInfo['name'], _appInfo['author'])


def _path(filename, cache):
    return os.path.join(_cachePath if cache else _dataPath, filename)


def _load(filename):
    import pickle
    try:
        with open(filename, 'rb') as file:
            return True, pickle.load(file)
    except:
        return False, None


def _store(filename, data):
    import pickle
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as file:
            pickle.dump(data, file)
    except:
        return False
    else:
        return True


def _delete(path):
    try:
        if os.path.isdir(path):
            import shutil
            shutil.rmtree(path)
        else:
            os.remove(path)
    except:
        return False
    else:
        return True


def loadCache(filename):
    return _load(_path(filename, True))


def loadCacheOr(filename, default=None):
    loaded, data = loadCache(filename)
    return data if loaded else default


def storeCache(filename, data):
    return _store(_path(filename, True), data)


def deleteCache(path):
    return _delete(_path(path, True))


def load(filename):
    return _load(_path(filename, False))


def loadOr(filename, default=None):
    loaded, data = load(filename)
    return data if loaded else default


def store(filename, data):
    return _store(_path(filename, False), data)


def delete(path):
    return _delete(_path(path, False))
