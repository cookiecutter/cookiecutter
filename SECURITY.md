# Security Policy

## Reporting a Vulnerability

If you find a security vulnerability in Cookiecutter, please report it through [GitHub's private vulnerability reporting](https://github.com/cookiecutter/cookiecutter/security/advisories/new). This keeps the details private while we work on a fix.

Please include:

- What you found and how to reproduce it
- Which version you're using
- Any relevant logs or output (redact secrets)

## Trust Model

Cookiecutter executes templates from sources the user specifies (GitHub repos, zip URLs). Templates can run arbitrary code through hook scripts (`pre_prompt`, `pre_gen_project`, `post_gen_project`), and Cookiecutter does not sandbox them. This is by design. Users are responsible for reviewing templates before running them.

## What's in Scope

- The `cookiecutter` CLI and Python API
- Jinja2 template rendering and variable handling
- Hook execution (`pre_gen_project`, `post_gen_project`, `pre_prompt`)
- Config file handling (`~/.cookiecutterrc`, `cookiecutter.json`)
- Git and zip-based template retrieval
- Hook execution awareness bypass (mechanisms that cause hooks to run without the user's knowledge)
- Template rendering exfiltration (vulnerabilities in the Jinja2 layer that leak data outside the expected output)

If you're unsure whether something qualifies, report it and we'll assess.

## What's Out of Scope

- Hook scripts executing arbitrary code (this is intended behavior, see Trust Model above)
- Malicious content in third-party templates (template authors are outside our trust boundary)
- Vulnerabilities in dependencies of generated projects (those belong to the template author)

## Security Measures

- **Dependabot** monitors GitHub Actions dependencies for known vulnerabilities
- **Least-privilege CI permissions** (`permissions: contents: read` at the workflow level)
- **Hook validation** only recognizes known hook names (`pre_prompt`, `pre_gen_project`, `post_gen_project`), rejecting unexpected scripts in the `hooks/` directory
- **Failed hook cleanup** automatically removes partially-generated project directories when a hook script fails, preventing incomplete output from being used

## Data Collection

Cookiecutter does not collect, store, or transmit any user data. There is no telemetry, analytics, or phone-home behavior of any kind.

## Response Times

This is a volunteer-maintained open source project. Security reports are taken seriously, but there are no guaranteed response times.

**Enterprise support** is available, with priority response SLAs. Contact support@feldroy.com for details.

## Supported Versions

Security fixes are applied to the latest release on the `main` branch. There is no backport policy for older versions.
