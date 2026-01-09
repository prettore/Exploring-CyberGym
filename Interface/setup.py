import sys
from setuptools import setup

with open('Requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="Interface",
    version=1,
    install_requires=requirements,
    description="A CybORG graphical user interface"
    )
