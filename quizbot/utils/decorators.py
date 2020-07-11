
class _ClassPropertyDescriptor:

    def __init__(self, f):
        self._f = f

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self._f.__get__(obj, klass)()

    def __set__(self, obj, value):
        raise AttributeError()

    def __delete__(self, obj):
        raise AttributeError()


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return _ClassPropertyDescriptor(func)
