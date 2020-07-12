
import random
from ..utils import range

topics = set()

answerCount = 4


def randomTopic():
    return random.sample(topics, 1)[0] if len(topics) > 0 else None


class Topic:

    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError('Unexpected name type')
        self._questions = set()
        self._name = name
        self._dependencies = set()
        topics.add(self)

    def _registerQuestion(self, question):
        self._questions.add(question)
        self._dependencies.update(question.dependencies)

    @property
    def name(self):
        return self._name

    @property
    def questions(self):
        return self._questions

    @property
    def allDependencies(self):
        return tuple(self._dependencies)

    @property
    def areAllReady(self):
        return all(d.isReady for d in self._dependencies)

    def readyAll(self):
        for d in self._dependencies:
            d.ready()

    def randomQuestionFactory(self, difficulty, includeNotReady=False):
        questions = [q for q in self._questions if q.difficultyRange.contains(difficulty) and (includeNotReady or q.isReady)]
        if len(questions) == 0:
            return None
        return random.choice(questions)

    def randomQuestion(self, difficulty, ready=False):
        question = self.randomQuestionFactory(difficulty, ready)
        question.ready()
        relativeDifficulty = question.difficultyRange.getProgress(difficulty)
        return question(relativeDifficulty)

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self._name)})'

    def __str__(self):
        return self._name


class QuestionFactory:

    def __init__(self, producer, topic, difficultyRange=(0, 1), dependencies=[]):
        if not isinstance(topic, Topic):
            raise TypeError('Unexpected topic type')
        if not callable(producer):
            raise TypeError('Unexpected producer type')
        if not isinstance(dependencies, (list, tuple, set)) or any(not isinstance(d, QuestionDependency) for d in dependencies):
            raise TypeError('Unexpected dependencies type')
        self._topic = topic
        self._difficultyRange = range.Range.ensure(difficultyRange)
        self._producer = producer
        self._dependencies = tuple(dependencies)
        topic._registerQuestion(self)

    def __call__(self, difficulty):
        if not isinstance(difficulty, (int, float)):
            raise TypeError('Unexpected difficulty type')
        if not self.isReady:
            raise RuntimeError('Not all dependencies are statisfied')
        return self._producer(range.clamp((0, 1), difficulty))

    def __repr__(self):
        return f'{self.__class__.__name__}{(self._producer, self._topic, self._difficultyRange, self._dependencies)}'

    def __str__(self):
        return self.producerName

    @property
    def producerName(self):
        return self._producer.__name__

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def isReady(self):
        return all(d.isReady for d in self._dependencies)

    def ready(self):
        for d in self._dependencies:
            d.ready()

    @property
    def topic(self):
        return self._topic

    @property
    def difficultyRange(self):
        return self._difficultyRange


class QuestionDependency:

    def __init__(self, func):
        self._ready = False
        self._func = func

    def __call__(self):
        self._ready = False
        try:
            self._func()
        except:
            raise DependencyError()
        else:
            self._ready = True

    def ready(self):
        if not self._ready:
            self()

    @property
    def functionName(self):
        return self._func.__name__

    @property
    def isReady(self):
        return self._ready

    def __repr__(self):
        return f'{self.__class__.__name__}({self._func})'

    def __str__(self):
        return self.functionName


class DependencyError(Exception):
    pass


def question(topic, difficultyRange=(0, 1), dependencies=[]):
    def wrapper(func):
        return QuestionFactory(func, topic, difficultyRange, dependencies)
    return wrapper


def dependency(func):
    return QuestionDependency(func)
