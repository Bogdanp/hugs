from setuptools import setup


with open("hugs/__init__.py") as module:
    version_marker = "__version__ = "
    for line in module:
        if line.startswith(version_marker):
            version = line[len(version_marker):].strip().strip('"')
            break
    else:
        assert False, "could not find version in hugs/__init__.py"


setup(
    name="hugs",
    version=version,
    description="Hugs lets you map SQL expressions to Python functions.",
    long_description="https://github.com/Bogdanp/hugs",
    packages=["hugs"],
    author="Bogdan Popa",
    author_email="popa.bogdanp@gmail.com",
    url="https://github.com/Bogdanp/hugs",
)
