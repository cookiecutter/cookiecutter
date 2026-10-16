"""Regression coverage for the unzip() half of cookiecutter issue #2278.

``unzip`` derived the cache filename from the raw URI
(``zip_uri.rsplit('/', 1)[1]``), so a URL with a query string produced a
filename containing ``?`` and ``&`` — not a valid path on any platform — while a
fragment was silently swallowed into the name. The name must come from the URL
*path*, and the full URL must still be what gets requested.
"""

from __future__ import annotations

from pathlib import Path

from cookiecutter import zipfile


def _fake_response():
    class _Resp:
        def iter_content(self, chunk_size=1024):
            with Path('tests/files/fake-repo-tmpl.zip').open('rb') as zf:
                chunk = zf.read(chunk_size)
                while chunk:
                    yield chunk
                    chunk = zf.read(chunk_size)

    return _Resp()


def _patch_get(mocker):
    return mocker.patch(
        'cookiecutter.zipfile.requests.get',
        return_value=_fake_response(),
        autospec=True,
    )


def test_unzip_caches_under_url_path_with_query(mocker, clone_dir) -> None:
    """A query string must not leak into the cache filename."""
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )
    get = _patch_get(mocker)

    output_dir = zipfile.unzip(
        'https://example.com/tmpl/fake-repo-tmpl.zip?token=abc123',
        is_url=True,
        clone_to_dir=str(clone_dir),
    )

    assert output_dir
    cached = sorted(p.name for p in Path(clone_dir).iterdir())
    assert cached == ['fake-repo-tmpl.zip'], cached
    assert get.call_args[0][0] == 'https://example.com/tmpl/fake-repo-tmpl.zip?token=abc123'


def test_unzip_caches_under_url_path_when_fragment_present(mocker, clone_dir) -> None:
    """A fragment must not leak into the cache filename either."""
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )
    get = _patch_get(mocker)

    output_dir = zipfile.unzip(
        'https://example.com/tmpl/fake-repo-tmpl.zip#subdir',
        is_url=True,
        clone_to_dir=str(clone_dir),
    )

    assert output_dir
    cached = sorted(p.name for p in Path(clone_dir).iterdir())
    assert cached == ['fake-repo-tmpl.zip'], cached
    assert get.call_args[0][0] == 'https://example.com/tmpl/fake-repo-tmpl.zip#subdir'


def test_unzip_plain_url_cache_name_is_unchanged(mocker, clone_dir) -> None:
    """The plain-URL cache filename keeps its existing value."""
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )
    _patch_get(mocker)

    zipfile.unzip(
        'https://example.com/tmpl/fake-repo-tmpl.zip',
        is_url=True,
        clone_to_dir=str(clone_dir),
    )

    cached = sorted(p.name for p in Path(clone_dir).iterdir())
    assert cached == ['fake-repo-tmpl.zip'], cached
