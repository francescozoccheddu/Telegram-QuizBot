
import os
import re


_scripts_dir = os.path.dirname(os.path.realpath(__file__))


def _path(folder):
    return os.path.join(_scripts_dir, '..', folder)


_resourcesPath = _path('resources')
_cachePath = _path('cache')
_dataPath = _path('data')
_jsonLinkRegex = re.compile(r'^(@(?P<link>[^@].*)|\?(?P<lazyLink>[^\?].*))$')


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


def _json(filename):
    import json
    return json.load(_file(_resourcesPath, filename, True))


def _linkJson(data, dirname, history):
    if isinstance(data, str):
        match = _jsonLinkRegex.match(data)
        link = match.group('link') if match is not None else None
        if link is not None:
            if not os.path.isabs(link):
                link = os.path.join(dirname, link)
            link = os.path.normpath(link)
            if link.lower().endswith('.json'):
                if link in history:
                    raise RecursionError('Resource cycle detected', link=link)
                return _linkJson(_json(link), os.path.dirname(link), history.union({link}))
            else:
                return text(link)
        else:
            lazyLink = match.group('lazyLink') if match is not None else None
            if lazyLink is not None and not os.path.isabs(lazyLink):
                return os.path.join(dirname, lazyLink)
    elif isinstance(data, dict):
        return {k: _linkJson(v, dirname, history) for k, v in data.items()}
    elif isinstance(data, list):
        return [_linkJson(v, dirname, history) for v in data]
    return data


def json(filename, link=True):
    data = _json(filename)
    if link:
        data = _linkJson(data, os.path.dirname(filename), {os.path.normpath(filename)})
    return data


def _load(path, filename):
    import pickle
    try:
        with _file(path, filename, True, True) as file:
            return True, pickle.load(file)
    except:
        return False, None


def _store(path, filename, data):
    import pickle
    try:
        with _file(_cachePath, filename, False, True) as file:
            pickle.dump(data, file)
    except:
        return False
    else:
        return True


def _delete(path, filename):
    realpath = os.path.join(path, filename)
    try:
        if os.path.isdir(path):
            import shutil
            shutil.rmtree(realpath)
        else:
            os.remove(realpath)
    except:
        return False
    else:
        return True


def loadCache(filename):
    return _load(_cachePath, filename)


def storeCache(filename, data):
    return _store(_cachePath, filename, data)


def deleteCache(path):
    return _delete(_cachePath, path)


def load(filename):
    return _load(_dataPath, filename)


def store(filename, data):
    return _store(_dataPath, filename, data)


def delete(path):
    return _delete(_dataPath, path)
