## Release Process

1. Set the version number in ``pyproject.toml`` and ``cookiecutter/__init__.py`` files, and commit the changes.
2. Create a new tag by running ``git tag <VERSION_NUMBER> -m '<MESSAGE>'`` then ``git push origin <VERSION_NUMBER>`` to push the new tag to GitHub.
3. Go to the releases page on GitHub and create a new release.
4. Once the release is created, a new workflow named 'Upload to PyPI' will start to build the package and publish it to the main repository on PyPI.
