import threading
import random
from ..utils import resources


_questionsByTopic = {}
_allQuestions = []
_datasets = None


def _getDataset(key):
    return _datasets.get(key, None) if _datasets is not None else None


def _getData(key):
    dataset = _getDataset(key)
    if dataset is None or not dataset.isReady:
        return None
    return dataset.data


def _registerQuestion(question):
    _allQuestions.append(question)
    topic = _questionsByTopic.get(question.topic, [])
    topic.append(question)
    _questionsByTopic[question.topic] = topic


_config = resources.json('config.json')


def answersCount():
    return _config['answersCount']


def topics():
    return tuple(_questionsByTopic.keys())


def questions(topics=None, includeNotReady=False):
    if isinstance(topics, str):
        topics = [topics]
    if topics is None or len(topics) == 0:
        return tuple(q for q in _allQuestions if includeNotReady or q.isReady)
    else:
        questions = set()
        for t in topics:
            qt = _questionsByTopic.get(t, [])
            questions.update(q for q in qt if includeNotReady or q.isReady)
        return tuple(questions)


def randomQuestion(difficulty=None, topics=None, includeNotReady=False):
    pool = questions(topics, includeNotReady)
    if len(pool) == 0:
        return None
    if difficulty is not None:
        if 0 > difficulty > 1:
            raise ValueError('Difficulty must fall in range [0,1]')

        def _weight(q):
            diff = 1 - abs(difficulty - q.difficulty)
            a, b = _config['probabilityPerDifficultyRange']
            return a + diff * (b - a)

        return random.sample(pool, weights=list(map(_weight, pool)))[0]
    else:
        return random.choice(pool)


def readyAllWithUI(reloadDescriptors=False):
    def plural(n):
        return 's' if n != 1 else ''
    if _datasets is None or reloadDescriptors:
        print('Loading datasets descriptors...')
        loadDatasets()
        ready = sum(1 for d in _datasets.values() if d.isReady)
        readyMessage = f' ({ready} dataset{plural(ready)} from cache)' if ready > 0 else ''
        print(f'Done loading {len(_datasets)} dataset descriptor{plural(len(_datasets))}{readyMessage}.')
    print('Collecting datasets... (This may take minutes)')
    from . import topics
    try:
        from tqdm import tqdm
    except ImportError:
        onProgress = None
        output = print
        bar = None
    else:
        bar = tqdm(total=None, bar_format='{percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}')

        def onProgress(p, t):
            bar.total = t
            bar.n = p
            bar.refresh()
        output = tqdm.write

    def onFailure(key, error):
        output(f'Exception while processing dataset "{key}": {error}')
    readyAllDatasets(onProgress, onFailure)
    if bar is not None:
        bar.close()
    nonready = sum(1 for d in _datasets.values() if not d.isReady)
    failsMessage = ' All datasets are ready.' if nonready == 0 else f' (Failed to collect {nonready} dataset{plural(nonready)}'
    print(f'Done.{failsMessage}')
    print('Caching datasets...')
    cacheDatasets()
    print('Done.')


def loadDatasets():
    from . import datasets
    filename = _config['datasetsFile']
    global _datasets
    _datasets = datasets.fromResource(filename, lambda t: '/'.join(t), _config['datasetsCacheFile'])


def cacheDatasets():
    from . import datasets
    datasets.cache(_datasets, _config['datasetsCacheFile'])


def readyAllDatasets(onProgress=None, onFailure=None):
    datasets = list((k, d) for k, d in _datasets.items() if not d.isReady)
    if onProgress is not None:
        onProgress(0, len(datasets))
    for i, t in enumerate(datasets):
        k, d = t
        try:
            d.ready()
        except Exception as e:
            if onFailure is not None:
                onFailure(k, e)
        if onProgress is not None:
            onProgress(i + 1, len(datasets))
