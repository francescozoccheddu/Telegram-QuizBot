from setuptools import setup

import os
_scripts_dir = os.path.dirname(os.path.realpath(__file__))
_requirements_file = os.path.join(_scripts_dir, 'requirements.txt')
_readme_file = os.path.join(_scripts_dir, 'README.md')

with open(_readme_file) as file:
    _readme = file.read()

with open(_requirements_file) as f:
    _requirements = f.read().splitlines()

setup(
    name='QuizBot',
    author='Francesco Zoccheddu',
    version='0.0.1',
    long_description=_readme,
    long_description_content_type='text/markdown',
    url='https://github.com/francescozoccheddu/telegram-quizbot',
    entry_points={
        'console_scripts': ['quizbot = quizbot.utils.launcher:main']
    },
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    packages=['quizbot'],
    install_requires=_requirements,
    python_requires='>=3.8'
)
