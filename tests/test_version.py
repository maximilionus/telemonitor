"""
Test app version values in all files to match
"""
import toml

from telemonitor import __version__


def get_toml() -> dict:
    with open('./pyproject.toml', 'rt') as f:
        toml_dict = toml.load(f)
    return toml_dict


def get_toml_version() -> str:
    version = get_toml()['tool']['poetry']['version']
    return version


def test_init_version():
    toml_version = get_toml_version()

    assert __version__ == toml_version, "Version is not up-to-date"
