#!/usr/bin/env python

from setuptools import setup


setup(
    name='untwiner',
    version='0.1.0',
    description='Python package for navigating the stories '
                'created in the Twine 2 program.',
    url='https://github.com/terentjew-alexey/untwiner',
    license='Apache 2.0',
    author='Aleksey Terentyev',
    author_email='terentjew.alexey@gmail.com',
    packages=['untwiner'],
    install_requires=[
        'lxml',
        'beautifulsoup4',
    ],
)
