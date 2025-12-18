import sys
sys.path.append("../CybORG/")
from pprint import pprint

from CybORG import CybORG
from CybORG.Simulator.Scenarios import FileReaderScenarioGenerator
from CybORG.Agents import B_lineAgent
from CybORG.Agents import BlueReactRemoveAgent
from CybORG.Agents import BlueReactRestoreAgent
from CybORG.Agents.Wrappers import RedTableWrapper
from CybORG.Agents.Wrappers.TrueTableWrapper import true_obs_to_table

path = "../CybORG/CybORG/Simulator/Scenarios/scenario_files/Scenario1b.yaml"
sg = FileReaderScenarioGenerator(path)

blue_agent = BlueReactRemoveAgent()
red_agent = B_lineAgent()

env = CybORG(scenario_generator=sg, agents={'Blue':blue_agent, 'Red':red_agent})

results = env.reset(agent='Red')
print(env.get_ip_map())

for i in range(30):
    
    red_obs = env.get_observation('Red')
    red_action = red_agent.get_action(observation=red_obs, action_space=env.get_action_space('Red'))
    results = env.step(action=red_action, agent='Red')
    red_obs = env.get_observation('Red')

    print("--- RED ---")
    print(red_action)
    pprint("Sucesso da ação: {}".format(red_obs.get('success')))

    blue_obs = env.get_observation('Blue')
    blue_action = blue_agent.get_action(blue_obs, env.get_action_space('Blue'))
    results = env.step(action=blue_action, agent='Blue')
    blue_obs = env.get_observation('Blue')
    
    print("--- BLUE ---")
    print(blue_action)
    pprint("Sucesso da ação: {}".format(blue_obs.get('success')))

    a = input("")
    print("\n\n")    
