from setuptools import setup, find_packages
from fmojinja.__version__ import get_version
from codecs import open
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="fmojinja",
    version=get_version(),
    url="https://github.com/physchemstar/fmojinja",
    description="A FMO-related programs' input generators and output readers package",
    author="Yusuke Kawashima",
    author_email="y-kawashima@hoshi.ac.jp",
    license="MIT",
    packages=find_packages(),
    package_data={},
    install_requires=["jinja2", "pandas", "numpy", "pyyaml"],
)