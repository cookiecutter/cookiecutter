.. Advanced Usage master index

Advanced Usage
==============

Various advanced topics regarding cookiecutter usage.

.. toctree::
   :maxdepth: 2

   hooks
   user_config
   calling_from_python
   injecting_context
   suppressing_prompts
   templates_in_context
   private_variables
   copy_without_render
   replay
   choice_variables
   boolean_variables
   dict_variables
   templates
   template_extensions
   directories
   jinja_env
   new_line_characters
   local_extensions
   nested_config_files
   human_readable_prompts

Running mypy and other static analysis tools
--------------------------------------------

Cookiecutter templates themselves are not valid Python projects. For example,
a module or directory named ``{{ cookiecutter.project_name }}`` cannot be
recognized as a valid Python package by tools such as ``mypy`` due to the
presence of template variables.

To use static analysis tools like ``mypy`` or ``ruff``, first generate a
project from the template and then run the tool on the **generated project**.

A common approach in tests is to use ``pytest-cookies`` to bake a project and
run checks on the resulting code::

    def test_project_passes_mypy(cookies):
        result = cookies.bake(extra_context={"project_name": "example_project"})
        assert result.exit_code == 0
        project_path = result.project

        completed = subprocess.run(
            ["mypy", "."],
            cwd=project_path,
            check=False,
        )
        assert completed.returncode == 0

This ensures that static analysis is performed on real generated code, not the
template files.
