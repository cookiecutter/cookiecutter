import missing_package


def pre_gen_project(project_dir, cookiecutter):
    cookiecutter['name'] = missing_package.name()
    cookiecutter['uuid'] = '123'
