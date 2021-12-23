# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages
from vrn7500tools import version

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = [line.rstrip() for line in f]

setup(
    name='vrn7500tools',
#    version=vrn7500tools.version(),
    version=version.version(),
    description='Utilities for converting CHIRP csv to channel groups into VR-N7500/RT99 mobile radios',
    long_description=readme,
    author='Konstantin Läufer',
    author_email='laufer@cs.luc.edu',
    url='https://github.com/klaeufer/vrn7500tools',
    license=license,
    python_requires='>=3',
    install_requires=requirements,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points = {
        'console_scripts': [
            'chirp2cg = vrn7500tools.chirp2cg:main'
        ]
    }
)
