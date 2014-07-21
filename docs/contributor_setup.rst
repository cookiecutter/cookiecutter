Setting Up the Code for Local Development
-----------------------------------------

Here's how to set up `cookiecutter` for local development.

1. Fork the `cookiecutter` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/cookiecutter.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv cookiecutter
    $ cd cookiecutter/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the tests and flake8::

    $ flake8 cookiecutter tests
    $ python setup.py test
    $ tox

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Check that the test coverage hasn't dropped::

    coverage run --source cookiecutter setup.py test
    coverage report -m
    coverage html

8. Submit a pull request through the GitHub website.