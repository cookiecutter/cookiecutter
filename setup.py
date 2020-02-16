#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""cookiecutter distutils configuration."""

import os
import io
import sys

from setuptools import setup

version = "1.7.0"

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

with io.open('README.md', 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

requirements = [
    'binaryornot>=0.2.0',
    'jinja2>=2.7',
    'click>=7.0',
    'poyo>=0.1.0',
    'jinja2-time>=0.1.0',
    'requests>=2.18.0',
    'six>=1.10',
]

if sys.argv[-1] == 'readme':
    print(readme)
    sys.exit()


setup(
    name='cookiecutter',
    version=version,
    description=('A command-line utility that creates projects from project '
                 'templates, e.g. creating a Python package project from a '
                 'Python package project template.'),
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Audrey Roy',
    author_email='audreyr@gmail.com',
    url='https://github.com/cookiecutter/cookiecutter',
    packages=[
        'cookiecutter',
    ],
    package_dir={'cookiecutter': 'cookiecutter'},
    entry_points={
        'console_scripts': [
            'cookiecutter = cookiecutter.__main__:main',
        ]
    },
    include_package_data=True,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    install_requires=requirements,
    extras_require={
        ':python_version<"3.3"': ['whichcraft>=0.4.0'],
    },
    license='BSD',
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development",
    ],
    keywords=(
        'cookiecutter, Python, projects, project templates, Jinja2, '
        'skeleton, scaffolding, project directory, setup.py, package, '
        'packaging'
    ),
)
