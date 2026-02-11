import sys
from setuptools import setup

with open('Requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="Parser",
    version=2.0,
    install_requires=requirements,
    description="A CybORG network parser for yaml files"
)
