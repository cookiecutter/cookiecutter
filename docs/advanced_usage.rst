==============
Advanced Usage
==============

Calling Cookiecutter Functions From Python
------------------------------------------

You can use Cookiecutter from Python::

    from cookiecutter.main import cookiecutter
    
    # Create project from the cookiecutter-pypackage/ template
    cookiecutter('cookiecutter-pypackage/')

    # Create project from the cookiecutter-pypackage.git repo template
    cookiecutter('https://github.com/audreyr/cookiecutter-pypackage.git')
    
See the :ref:`API Reference` for more details.

If you use it in an interesting way, I'd love to hear about it: file an issue,
please!
