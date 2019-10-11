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
    include_package_data=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Environment :: Other Environment',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries'
    ]
)
