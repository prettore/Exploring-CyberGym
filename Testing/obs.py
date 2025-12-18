import random
import inspect
from os.path import dirname
from pprint import pprint

from CybORG import CybORG
from CybORG.Simulator.Scenarios import FileReaderScenarioGenerator
from CybORG.Agents import B_lineAgent

path = inspect.getfile(CybORG)
path = dirname(path) + f'/Simulator/Scenarios/scenario_files/Scenario1b.yaml'
sg = FileReaderScenarioGenerator(path)

# cyborg = CybORG(scenario_generator=sg)

env = CybORG(sg)

results = env.reset(agent='Red')
print(results)
obs = results.observation

print('Red observations:')
pprint(obs['User0'])

blue_obs = env.get_observation(agent='Blue')

print('\nBlue observations: ')
pprint(blue_obs)
