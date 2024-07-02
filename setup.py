"""cookiecutter distutils configuration."""

from pathlib import Path

from setuptools import setup


def _get_version() -> str:
    """Read cookiecutter/VERSION.txt and return its contents."""
    path = Path("cookiecutter").resolve()
    version_file = path / "VERSION.txt"
    return version_file.read_text().strip()


version = _get_version()


with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()


requirements = [
    'binaryornot>=0.4.4',
    'Jinja2>=2.7,<4.0.0',
    'click>=7.0,<9.0.0',
    'pyyaml>=5.3.1',
    'python-slugify>=4.0.0',
    'requests>=2.23.0',
    'arrow',
    'rich',
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
    project_urls={
        "Documentation": "https://cookiecutter.readthedocs.io",
        "Issues": "https://github.com/cookiecutter/cookiecutter/issues",
        "Discord": "https://discord.gg/9BrxzPKuEW",
    },
    packages=['cookiecutter'],
    package_dir={'cookiecutter': 'cookiecutter'},
    entry_points={'console_scripts': ['cookiecutter = cookiecutter.__main__:main']},
    include_package_data=True,
    python_requires='>=3.7',
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
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
