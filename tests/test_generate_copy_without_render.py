def test_generate_copy_without_render_extensions(self):
    generate.generate_files(
        context={
            'cookiecutter': {
                "repo_name": "test_copy_without_render",
                "render_test": "I have been rendered!",
                "_copy_without_render": [
                    "*not-rendered",
                    "rendered/not_rendered.yml",
                    "*.txt",
                ]}
        },
        repo_dir='tests/test-generate-copy-without-render'
    )

    self.assertIn("{{cookiecutter.repo_name}}-not-rendered",
                  os.listdir("test_copy_without_render"))
    self.assertIn("test_copy_without_render-rendered",
                  os.listdir("test_copy_without_render"))

    with open("test_copy_without_render/README.txt") as f:
        self.assertIn("{{cookiecutter.render_test}}", f.read())

    with open("test_copy_without_render/README.rst") as f:
        self.assertIn("I have been rendered!", f.read())

    with open("test_copy_without_render/test_copy_without_render-rendered/README.txt") as f:
        self.assertIn("{{cookiecutter.render_test}}", f.read())

    with open("test_copy_without_render/test_copy_without_render-rendered/README.rst") as f:
        self.assertIn("I have been rendered", f.read())

    with open("test_copy_without_render/{{cookiecutter.repo_name}}-not-rendered/README.rst") as f:
        self.assertIn("{{cookiecutter.render_test}}", f.read())

    with open("test_copy_without_render/rendered/not_rendered.yml") as f:
        self.assertIn("{{cookiecutter.render_test}}", f.read())

    if os.path.exists('test_copy_without_render'):
        shutil.rmtree('test_copy_without_render')
