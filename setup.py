#!/usr/bin/env python

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

requirements = ['binaryornot>=0.2.0', 'jinja2>=2.4', 'PyYAML>=3.10']
test_requirements = []

# Add Python 2.6-specific dependencies
if sys.version_info[:2] < (2, 7):
    requirements.append('argparse')
    requirements.append('ordereddict')
    requirements.append('simplejson')
    test_requirements.append('unittest2')

# Add Python 2.6 and 2.7-specific dependencies
if sys.version < '3':
    test_requirements.append('mock')

# There are no Python 3-specific dependencies to add

setup(
    name='cookiecutter',
    version='0.7.1',
    description=('A command-line utility that creates projects from project '
                 'templates, e.g. creating a Python package project from a Python '
                 'package project template.'),
    long_description=readme + '\n\n' + history,
    author='Audrey Roy',
    author_email='audreyr@gmail.com',
    url='https://github.com/audreyr/cookiecutter',
    packages=[
        'cookiecutter',
    ],
    package_dir={'cookiecutter': 'cookiecutter'},
    entry_points={
        'console_scripts': [
            'cookiecutter = cookiecutter.main:main',
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license='BSD',
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    keywords='cookiecutter, Python, projects, project templates, Jinja2, \
        skeleton, scaffolding, project directory, setup.py, package, packaging',
    test_suite='tests',
    tests_require=test_requirements
)
