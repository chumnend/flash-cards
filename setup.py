#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='flash-cards',
    version='2.0.0',
    description='Flash Cards Application',
    author='Nicholas Chumney',
    author_email='nicholas.chumney@outlook.com',
    packages=find_packages(),
    scripts=['manage.py'],
)
