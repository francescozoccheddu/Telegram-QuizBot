from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop

import os
_scripts_dir = os.path.dirname(os.path.realpath(__file__))
_requirements_file = os.path.join(_scripts_dir, 'requirements.txt')
_readme_file = os.path.join(_scripts_dir, 'README.md')

with open(_readme_file, 'r') as file:
    _readme = file.read()

with open(_requirements_file) as f:
    _requirements = f.read().splitlines()


def runPostInstall():
    print('Running post install script')
    import postinstall
    postinstall.run()


class InstallCommand(install):

    def run(self):
        install.run(self)
        runPostInstall()


class DevelopCommand(develop):

    def run(self):
        develop.run(self)
        runPostInstall()


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
    cmdclass={
        'install': InstallCommand,
        'develop': DevelopCommand
    },
    install_requires=_requirements
)
