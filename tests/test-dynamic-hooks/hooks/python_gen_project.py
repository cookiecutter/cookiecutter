from uuid import uuid4


def pre_gen_project(project_dir, cookiecutter):
    cookiecutter['name'] = 'Archibald'
    cookiecutter['uuid'] = str(uuid4())
