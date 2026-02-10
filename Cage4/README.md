# CybORG installation

These steps differ from the original guide for they fix numpy dependency, also creating a virtual environment is highly recommended.
Feel free to use anaconda, although this is a slower approach.

Use pyenv version management tool and install python 3.10
Ensure you are at the project root
```
pyenv install 3.10
pyenv local 3.10
```
Create a virtual environment and install dependencies
```
python -m venv .venv &&
echo 'export PYTHONPATH=$PYTHONPATH:/path/to/repo/Exploring-CyberGym/Cage4/cage-challenge-4' >> .venv/bin/activate
source .venv/bin/activate &&
pip install -U pip &&
cd cage-challenge-4 &&
pip install -e .
```
Test if everything works correctly
```
pytest
```
The original instructions are found on [https://github.com/cage-challenge/CybORG/blob/2742b5e0ce4330c9b14006b38acd3b5ebe00d6fd/CybORG/Tutorial/0.%20Installation.](https://github.com/cage-challenge/CybORG
