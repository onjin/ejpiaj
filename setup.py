#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='ejpiaj',
    version='0.3.0',
    description='ejpiaj',
    long_description=readme + '\n\n' + history,
    author='Marek Wywiał',
    author_email='onjinx@gmail.com',
    url='https://github.com/onjin/ejpiaj',
    packages=[
        'ejpiaj',
    ],
    package_dir={'ejpiaj': 'ejpiaj'},
    include_package_data=True,
    install_requires=[
        'requests',
        'simplejson',
        'clint',
        'baker',
        'pyyaml',
    ],
    license="BSD",
    zip_safe=False,
    keywords='ejpiaj',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
    scripts=['ejpiaj/ejpiaj-cli'],
)
