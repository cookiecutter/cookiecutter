"""Simple pre-prompt hook that will fail if a specific env var is set."""
from pathlib import Path
import os
import sys


def backup_configuration(cwd: Path) -> Path:
    """Create a backup of cookiecutter.json."""
    src_data = (cwd / 'cookiecutter.json').read_text()
    dst = cwd / '_cookiecutter.json'
    with open(dst, 'w') as fh:
        fh.write(src_data)
    return dst


def main():
    """Check if we can run the  cookiecutter."""
    if os.environ.get("COOKIECUTTER_FAIL_PRE_PROMPT", False):
        sys.exit(1)
    cwd = Path('.').resolve()
    bkp = backup_configuration(cwd)
    print(f"All good here, created {bkp}")


if __name__ == "__main__":
    main()
