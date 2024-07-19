import argparse
# from cookie_cutter_script import cookiecutter

from cookiecutter.main import cookiecutter as cookie
import cookiecutter.extensions

def run(project_name, repo_name, author_name, email, open_source_license):

    output_directory = '/path/to/your/desired/directory'

    context = {
        'project_name': project_name,
        'repo_name': repo_name,
        'author_name': author_name,
        'email': email,
        'version': '0.1.0',
        'open_source_license': open_source_license
    }
    cookie(
        'gh:audreyfeldroy//cookiecutter-pypackage', 
        no_input=True, 
        extra_context=context
        )

    print('Generated new project using cookiecutter.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Description of your program")

    parser.add_argument("--project_name", type=str)
    parser.add_argument("--repo_name", type=str)
    parser.add_argument("--author_name", type=str)
    parser.add_argument("--email", type=str)
    parser.add_argument("--open_source_license", type=str)
    # parser.add_argument("--llm_max_new_tokens", type=int)

    args = parser.parse_args()

    run(
        project_name=args.project_name,
        repo_name=args.repo_name, 
        author_name=args.author_name, 
        email=args.email, 
        open_source_license=args.open_source_license, 
        )