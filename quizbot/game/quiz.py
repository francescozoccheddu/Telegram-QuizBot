import threading
import random
from ..utils import resources


topics = set()

_config = resources.json('config.json')
_probabilityPerDifficultyRange = _config['probabilityPerDifficultyRange']
answersCount = _config['answersCount']


def randomTopic():
    return random.sample(topics, 1)[0] if len(topics) > 0 else None


def readyAllDependenciesWithUI():
    from ..utils import progress
    print('Processing quiz topics dependencies. This may take minutes.')
    progress.ui(readyAllDependencies, 'topics')


def readyAllDependencies(task=None):
    if task is not None:
        tasks = task.split(names=[t.name for t in topics])
    for i, t in enumerate(topics):
        t.readyAllDependencies(tasks[i] if task is not None else None)


class Topic:

    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError('Unexpected name type')
        self._questions = set()
        self._name = name
        topics.add(self)

    def _registerQuestion(self, question):
        self._questions.add(question)

    @property
    def name(self):
        return self._name

    @property
    def questions(self):
        return self._questions

    def readyAllDependencies(self, task=None):
        dependencies = set()
        for q in self._questions:
            dependencies.update(q.dependencies)
        dependencies = set(filter(lambda d: not d.isReady, dependencies))
        if task is not None:
            if len(dependencies) > 0:
                task.stepCount = len(dependencies)
            else:
                task.done()
        for d in dependencies:
            try:
                d()
            except Exception as e:
                if task is not None:
                    task.error(f'Exception on dependency "{d.producerName}": {repr(e)}')
            if task is not None:
                task.nextStep()

    def randomQuestionFactory(self, difficulty, includeNotReady=False):
        if 0 > difficulty > 1:
            raise ValueError('Difficulty must fall in range [0,1]')
        questions = [q for q in self._questions if (includeNotReady or q.isReady)]

        def _weight(question):
            diff = 1 - abs(difficulty - question.difficulty)
            a, b = _probabilityPerDifficultyRange
            return a + diff * (b - a)
        if len(questions) == 0:
            return None
        return random.choices(questions, weights=list(map(_weight, questions)))[0]

    def randomQuestion(self, difficulty, readyIfNotYet=False):
        question = self.randomQuestionFactory(difficulty, readyIfNotYet)
        question.ready()
        return question()

    def __repr__(self):
        return f'{self.__class__.__qualname__}({repr(self._name)})'

    def __str__(self):
        return self._name


class QuestionFactory:

    def __init__(self, producer, topic, difficulty=0.5, dependencies=[]):
        if not isinstance(topic, Topic):
            raise TypeError('Unexpected topic type')
        if not callable(producer):
            raise TypeError('Unexpected producer type')
        if not isinstance(dependencies, (list, tuple, set)) or any(not isinstance(d, QuestionDependency) for d in dependencies):
            raise TypeError('Unexpected dependencies type')
        if not isinstance(difficulty, (float, int)):
            raise TypeError('Unexpected difficulty type')
        if 0 > difficulty > 1:
            raise ValueError('Difficulty must fall in range [0,1]')
        self._topic = topic
        self._difficulty = difficulty
        self._producer = producer
        self._dependencies = dependencies
        topic._registerQuestion(self)

    def __call__(self):
        if not self.isReady:
            raise RuntimeError('Not all dependencies are ready')
        return self._producer()

    def __repr__(self):
        return f'{self.__class__.__qualname__}{(self._producer, self._topic, self._difficulty, self._dependencies)}'

    def __str__(self):
        return self.producerName

    @property
    def producerName(self):
        return f'{self._producer.__module__}.{self._producer.__qualname__}'

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def isReady(self):
        return all(d.isReady for d in self._dependencies)

    def ready(self, task=None):
        for d in self._dependencies:
            d()

    @property
    def topic(self):
        return self._topic

    @property
    def difficulty(self):
        return self._difficulty


class QuestionDependency:

    def __init__(self, producer, cache=False):
        if not isinstance(cache, bool):
            raise TypeError('Unexpected cache type')
        if not callable(producer):
            raise TypeError('Unexpected producer type')
        self._ready = False
        self._producer = producer
        self._data = None
        self._cache = cache
        self._lock = threading.Lock()

    def __call__(self, task=None):
        with self._lock:
            if not self._ready:
                from ..utils import resources
                if self._cache is not None:
                    cacheFile = f'.{self.__class__.__qualname__}_cache/{self.producerName}'
                    self._ready, self._data = resources.loadCache(cacheFile)
                if not self._ready:
                    try:
                        self._data = self._producer()
                    except Exception as e:
                        if task is not None:
                            task.fail(e)
                        raise
                    else:
                        if task is not None:
                            task.done()
                        if self._cache:
                            resources.storeCache(cacheFile, self._data)
                        self._ready = True
            return self._data

    @property
    def data(self):
        if not self._ready:
            raise RuntimeError('Not ready')
        return self._data

    @property
    def producerName(self):
        return f'{self._producer.__module__}.{self._producer.__qualname__}'

    @property
    def isReady(self):
        return self._ready

    def __repr__(self):
        return f'{self.__class__.__qualname__}({self._producer})'

    def __str__(self):
        return self.producerName


def question(topic, difficulty=0.5, dependencies=[]):
    def wrapper(producer):
        return QuestionFactory(producer, topic, difficulty, dependencies)
    return wrapper


def dependency(producer):
    return QuestionDependency(producer)


def cachedDependency(producer):
    return QuestionDependency(producer, True)
