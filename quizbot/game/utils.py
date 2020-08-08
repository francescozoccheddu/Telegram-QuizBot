
_strings = None


def _loadStrings():
    global _strings
    if _strings is None:
        from ..utils import strings
        _strings = strings.fromResource('strings/game.json')


def string(key):
    _loadStrings()
    return _strings[key]
