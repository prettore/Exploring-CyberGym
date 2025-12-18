# Exploring-CyberGym
This project aims to analyse and extend the CybORG research environment.

# CybORG Operations Research Gym
"A cyber security research environment for training and development of security human and autonomous agents. Contains a common interface for both emulated, using cloud based virtual machines, and simulated network environments."

# CybORG installation

These steps differ from the original guide for they fix numpy dependency, also creating a virtual environment is highly recommended.
Feel free to use anaconda, although this is a slower approach.

Use pyenv version management tool and install python 3.8.11
Ensure you are at the project root
'''
pyenv install 3.8.11
pyenv local 3.8.11
'''
Create a virtual environment and install dependencies
'''
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install numpy==1.21.6
'''

The original instructions are found here https://github.com/cage-challenge/CybORG/blob/2742b5e0ce4330c9b14006b38acd3b5ebe00d6fd/CybORG/Tutorial/0.%20Installation.md
