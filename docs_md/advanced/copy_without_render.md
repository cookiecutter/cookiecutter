---
title: Copy without Render
---

*New in Cookiecutter 1.1*

To avoid rendering directories and files of a cookiecutter, the
[\_copy\_without\_render]{.title-ref} key can be used in the
[cookiecutter.json]{.title-ref}. The value of this key accepts a list of
Unix shell-style wildcards:

    {
        "project_slug": "sample",
        "_copy_without_render": [
            "*.html",
            "*not_rendered_dir",
            "rendered_dir/not_rendered_file.ini"
        ]
    }
