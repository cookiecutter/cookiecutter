# -*- coding: utf-8 -*-
import io
import os

from cookiecutter import repository


def test_should_find_existing_cookiecutter(user_config_data):
    template = 'cookiecutter-pytest-plugin'
    cookiecutters_dir = user_config_data['cookiecutters_dir']
    cloned_template_path = os.path.join(cookiecutters_dir, template)
    os.mkdir(cloned_template_path)
    io.open(os.path.join(cloned_template_path, 'cookiecutter.json'), 'w')

    project_dir = repository.determine_repo_dir(
        template,
        abbreviations={},
        clone_to_dir=cookiecutters_dir,
        checkout=None,
        no_input=True,
    )

    assert cloned_template_path == project_dir
