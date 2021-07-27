from setuptools import setup, find_packages
from fmojinja.__version__ import get_version

setup(
    name="fmojinja",
    version=get_version(),
    license="MIT",
    packages=find_packages(),
    package_data={},
    install_requires=["jinja2", "pandas", "numpy", "pyyaml"],
)