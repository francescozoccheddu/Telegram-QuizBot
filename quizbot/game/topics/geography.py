from ..quizzes import Topic, question
from ...utils import range

topic = Topic("geography")


@question(topic, (0, 1))
def question1(difficulty):
    print(f"Question 1 with difficulty={difficulty}")


@question(topic, (0, 0.5))
def question2(difficulty):
    print(f"Question 2 with difficulty={difficulty}")


@question(topic, (0.5, 1))
def question3(difficulty):
    print(f"Question 3 with difficulty={difficulty}")


@question(topic, (0, 1))
def question4(difficulty):
    print(f"Question 4 with difficulty={difficulty}")
