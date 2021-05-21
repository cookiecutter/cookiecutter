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

setup(
    name='cookiecutter',
    version=version,
    description=(
        'A command-line utility that creates projects from project '
        'templates, e.g. creating a Python package project from a '
        'Python package project template.'
    ),
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Audrey Feldroy',
    author_email='audreyr@gmail.com',
    url='https://github.com/cookiecutter/cookiecutter',
    packages=['cookiecutter'],
    package_dir={'cookiecutter': 'cookiecutter'},
    entry_points={'console_scripts': ['cookiecutter = cookiecutter.__main__:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=requirements,
    license='BSD',
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
    keywords=[
        "cookiecutter",
        "Python",
        "projects",
        "project templates",
        "Jinja2",
        "skeleton",
        "scaffolding",
        "project directory",
        "package",
        "packaging",
    ],
)
