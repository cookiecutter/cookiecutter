#!/usr/bin/env python

import os
import sys

import cookiecutter

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst', 'rt').read()
history = open('HISTORY.rst', 'rt').read()
license = open('LICENSE', 'rt').read()

setup(
    name='cookiecutter',
    version=cookiecutter.__version__,
    description='Utility to render a directory of Jinja2 templates to files.',
    long_description=readme + '\n\n' + history,
    author='Audrey Roy',
    author_email='audreyr@gmail.com',
    url='https://github.com/audreyr/border',
    packages=[
        'cookiecutter',
    ],
    entry_points={
        'console_scripts': [
            'cookiecutter = cookiecutter.cookiecutter:command_line_runner',
        ]
    },
    include_package_data=True,
    install_requires=[
        'Jinja2',
    ],
    license=license,
    zip_safe=False,
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        "Environment :: Console",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ),
    keywords='cookiecutter Jinja2 templates project',
)
