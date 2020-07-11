
import abc
import asyncio
import random
from ..utils import decorators, range

topics = set()


def randomTopic():
    return random.sample(topics, 1)[0] if len(topics) > 0 else None


class Topic:

    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("Unexpected name type")
        self._questions = set()
        self._name = name
        topics.add(self)

    def _registerQuestion(self, quiz):
        self._questions.add(quiz)

    @property
    def name(self):
        return self._name

    @property
    def questions(self):
        return self._questions

    def randomQuestion(self, difficulty):
        questions = [q for q in self._questions if q.difficultyRange.contains(difficulty)]
        if len(questions) == 0:
            return None
        question = random.choice(questions)
        relativeDifficulty = question.difficultyRange.getProgress(difficulty)
        return question(relativeDifficulty)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self._name)})"


class QuestionFactory:

    def __init__(self, topic, difficultyRange, producer):
        if not isinstance(topic, Topic):
            raise TypeError("Unexpected topic type")
        if not callable(producer):
            raise TypeError("Unexpected producer type")
        self._topic = topic
        self._difficultyRange = range.Range.ensure(difficultyRange)
        self._producer = producer
        topic._registerQuestion(self)

    def __call__(self, difficulty):
        if not isinstance(difficulty, (int, float)):
            raise TypeError("Unexpected difficulty type")
        return self._producer(range.clamp((0, 1), difficulty))

    def __repr__(self):
        return f"{self.__class__.__name__}{(self._topic, self._difficultyRange, self._producer)}"

    @property
    def topic(self):
        return self._topic

    @property
    def difficultyRange(self):
        return self._difficultyRange


def question(topic, difficultyRange):
    def wrapper(func):
        return QuestionFactory(topic, difficultyRange, func)
    return wrapper
