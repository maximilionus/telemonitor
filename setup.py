from setuptools import setup


path_telemonitor_init = './telemonitor/__init__.py'


def get_project_version() -> str:
    nspace = {}
    with open(path_telemonitor_init, 'r') as f:
        exec(f.read(), nspace)

    return nspace["__version__"]


setup(
    name="telemonitor",
    version=get_project_version(),
    author="maximilionus",
    packages=["telemonitor"]
)
