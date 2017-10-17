#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='todoapp',
    version='0.0.1',
    description='A simple To-Do list app',
    author='Elias Dorneles',
    author_email='eliasdorneles@gmail.com',
    license='BSD license',
    packages=find_packages(
        exclude=['docs', 'tests', 'android']
    ),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD license',
    ],
    install_requires=[
    ],
    options={
        'app': {
            'formal_name': 'TodoApp',
            'bundle': 'org.pybee.elias'
        },
    }
)
