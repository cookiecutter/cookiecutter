.. _tutorial2:

==================================
Create a Cookieninja From Scratch
==================================

In this tutorial, we are creating `cookieninja-website-simple`, a cookieninja for generating simple, bare-bones websites.

Step 1: Name Your Cookieninja
------------------------------

Create the directory for your cookieninja and cd into it:

.. code-block:: bash

    $ mkdir cookieninja-website-simple
    $ cd cookieninja-website-simple/

Step 2: Create cookiecutter.json
----------------------------------

`cookiecutter.json` is a JSON file that contains fields which can be referenced in the cookieninja template. For each, default value is defined and user will be prompted for input during cookieninja execution. Only mandatory field is `project_slug` and it should comply with package naming conventions defined in `PEP8 Naming Conventions <https://www.python.org/dev/peps/pep-0008/#package-and-module-names>`_ .

.. code-block:: json

    {
      "project_name": "Cookiecutter Website Simple",
      "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '_') }}",
      "author": "Anonymous"
    }


Step 3: Create project_slug Directory
---------------------------------------

Create a directory called `{{ cookiecutter.project_slug }}`.

This value will be replaced with the repo name of projects that you generate from this cookieninja.

Step 4: Create index.html
--------------------------

Inside of `{{ cookiecutter.project_slug }}`, create `index.html` with following content:

.. code-block:: html

    <!doctype html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>{{ cookiecutter.project_name }}</title>
        </head>

        <body>
            <h1>{{ cookiecutter.project_name }}</h1>
            <p>by {{ cookiecutter.author }}</p>
        </body>
    </html>

Step 5: Pack cookiecutter into ZIP
----------------------------------
There are many ways to run Cookieninja templates, and they are described in details in `Usage chapter <https://cookiecutter.readthedocs.io/en/latest/usage.html#grab-a-cookiecutter-template>`_. In this tutorial we are going to ZIP cookieninja and then run it for testing.

By running following command `cookiecutter.zip` will get generated which can be used to run cookiecutter. Script will generate `cookiecutter.zip` ZIP file and echo full path to the file.

.. code-block:: bash

   $ (SOURCE_DIR=$(basename $PWD) ZIP=cookiecutter.zip && # Set variables
   pushd && # Set parent directory as working directory
   zip -r $ZIP $SOURCE_DIR --exclude $SOURCE_DIR/$ZIP --quiet && # ZIP cookiecutter
   mv $ZIP $SOURCE_DIR/$ZIP && # Move ZIP to original directory
   popd && # Restore original work directory
   echo  "Cookiecutter full path: $PWD/$ZIP")

Step 6: Run cookieninja
------------------------
Set your work directory to whatever directory you would like to run cookieninja at. Use cookieninja full path and run the following command:

.. code-block:: bash

   $ cookieninja <replace with Cookieninja full path>

You can expect similar output:

.. code-block:: bash

   $ cookieninja /Users/admin/cookiecutter-website-simple/cookiecutter.zip
   project_name [Cookiecutter Website Simple]: Test web
   project_slug [test_web]:
   author [Anonymous]: Cookiecutter Developer

Resulting directory should be inside your work directory with a name that matches `project_slug` you defined. Inside that directory there should be `index.html` with generated source:

.. code-block:: html

    <!doctype html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>Test web</title>
        </head>

        <body>
            <h1>Cookiecutter Developer</h1>
            <p>by Test web</p>
        </body>
    </html>
