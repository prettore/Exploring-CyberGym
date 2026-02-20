import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAGE_ROOT = os.path.join(BASE_DIR, "..", "cage-challenge-1")
sys.path.insert(0, CAGE_ROOT)

from CybORG import CybORG
print("Cage2 working")