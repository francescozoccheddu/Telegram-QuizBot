from ..utils.resources import Config
from ..quiz.holder import Holder, makeAutoRegisteringDecorator

_config = Config('configs/questions.json')
_quiz = Holder()
_loaded = False


def load(output=True, outputFailures=True):
    global _loaded
    from .topics import geography, movies, music, science
    from ..quiz.utils import loadAndReady, separatorKeyProvider
    datasets = _quiz.datasets if _loaded else _config.datasetsFile
    cacheFile = _config.datasetsCacheFile
    _quiz.datasets = loadAndReady(datasets, cacheFile=cacheFile, output=output, outputFailures=outputFailures)
    _loaded = True


question = makeAutoRegisteringDecorator(_quiz)


def quiz():
    return _quiz


def answersCount():
    return _config.answersCount
