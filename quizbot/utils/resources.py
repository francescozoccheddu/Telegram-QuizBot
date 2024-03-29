import re
import os

_root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
_resourcesPath = os.path.join(_root_dir, 'resources')


def _json(filename):
    import json
    with open(os.path.join(_resourcesPath, filename), 'r') as file:
        return json.load(file)


_jsonLinkRegex = re.compile(r'^(@(?P<link>[^@].*)|\?(?P<lazyLink>[^\?].*))$')


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


def text(filename):
    with open(os.path.join(_resourcesPath, filename), 'r') as file:
        return file.read()


def json(filename, link=True):
    data = _json(filename)
    if link:
        data = _linkJson(data, os.path.dirname(filename), {os.path.normpath(filename)})
    return data


class LazyResource:

    def __init__(self, filename):
        self._filename = filename
        self._loaded = False
        self._data = None

    def _load(self, filename):
        raise NotImplementedError()

    @property
    def data(self):
        if not self._loaded:
            self._data = self._load(self._filename)
        return self._data


class LazyJson(LazyResource):

    def __init__(self, filename):
        super().__init__(filename)

    def _load(self, filename):
        return json(filename)

    def __getitem__(self, key):
        return self.data[key]

    def __getattr__(self, name):
        return self.data[name]
