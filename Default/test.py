import random
from pprint import pprint
import matplotlib.pyplot as plt
import networkx as nx
from CybORG import CybORG
from CybORG.Simulator.Scenarios import FileReaderScenarioGenerator
import os

sg = FileReaderScenarioGenerator("./Scenarios/Scenario1b.yaml")
env = CybORG(sg)

state = env.environment_controller.state

G = state.link_diagram

nx.draw(G, with_labels=True)
plt.show()
