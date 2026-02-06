from setuptools import setup, find_packages

setup(
    name="CyberGUI",
    version="0.1.0",
    description="GUI for CybORG",
    author="gabarel707",
    packages=find_packages(),  # encontra automaticamente os pacotes
    install_requires=[
        "flask",
        "Flask-SQLAlchemy",
        "Flask-Migrate"
    ],
    python_requires=">=3.8",
)

