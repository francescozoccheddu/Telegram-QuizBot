from ..utils.resources import Config

_config = Config('configs/questions.json')
_quiz = None
_loaded = False


def load(output=True, outputFailures=True):
    global _loaded
    from .topics import geography, movies, music, science
    from ..quiz.utils import loadAndReady, separatorKeyProvider
    datasets = _quiz.datasets if _loaded else _config.datasetsFile
    cacheFile = _config.datasetsCacheFile
    _quiz.datasets = loadAndReady(datasets, cacheFile=cacheFile, output=output, outputFailures=outputFailures)
    _loaded = True


def question(topic, datasets=[]):
    from ..quiz.question import Question

    def wrapper(func):
        q = Question(func, topic, datasets)
        global _quiz
        if _quiz is None:
            from ..quiz.holder import Holder
            _quiz = Holder()
        _quiz.registerQuestion(q)
        return q
    return wrapper


def quiz():
    return _quiz


def answersCount():
    return _config.answersCount
