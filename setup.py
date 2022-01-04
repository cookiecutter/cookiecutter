#!/usr/bin/env python
"""cookiecutter distutils configuration."""
from setuptools import setup

version = "2.0.0"

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

requirements = [
    'binaryornot>=0.4.4',
    'Jinja2>=2.7,<4.0.0',
    'click>=7.0,<8.0.0',
    'pyyaml>=5.3.1',
    'jinja2-time>=0.2.0',
    'python-slugify>=4.0.0',
    'requests>=2.23.0',
]
