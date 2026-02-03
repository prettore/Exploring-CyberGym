import sys
sys.path.append('../CybORG')
from pprint import pprint


# IMPORTANDO O DEBBUGER
from CybORG.Agents.Wrappers.TrueTableWrapper import true_obs_to_table

from CybORG import CybORG
from CybORG.Simulator.Scenarios import FileReaderScenarioGenerator
from CybORG.Agents import B_lineAgent

path = f'../CybORG/CybORG/Simulator/Scenarios/scenario_files/Scenario1b.yaml'
sg = FileReaderScenarioGenerator(path)
env = CybORG(scenario_generator=sg, agents={'Red':B_lineAgent()})

results = env.reset(agent='Blue')

true_state = env.get_agent_state('True')

true_table = true_obs_to_table(true_state, env)
print(true_table)

for i in range(4):
    env.step()
    true_state = env.get_agent_state('True')
    true_table = true_obs_to_table(true_state, env)
    print(env.get_last_action('Red'))
    print(true_table)
    print(76*'-')
