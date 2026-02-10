# CybORG installation

These steps differ from the original guide for they fix numpy dependency, also creating a virtual environment is highly recommended.
Feel free to use anaconda, although this is a slower approach.

Use pyenv version management tool and install python 3.8.11
Ensure you are at the project root
```
pyenv install 3.8.11
pyenv local 3.8.11
```
Create a virtual environment and install dependencies
```
python -m venv .venv &&
echo 'export PYTHONPATH=$PYTHONPATH:/path/to/repo/Exploring-CyberGym/Cage2/cage-challenge-2' >> .venv/bin/activate
source .venv/bin/activate &&
pip install -U pip &&
pip install numpy==1.21.6 termcolor &&
cd CybORG &&
pip install -e .
```
Test if everything works correctly
```
pytest
```
The original instructions are found on [https://github.com/cage-challenge/CybORG/blob/2742b5e0ce4330c9b14006b38acd3b5ebe00d6fd/CybORG/Tutorial/0.%20Installation.](https://github.com/cage-challenge/CybORG
