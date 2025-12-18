
import sys
sys.path.append("../CybORG/")
from pprint import pprint

from CybORG import CybORG
from CybORG.Simulator.Scenarios import FileReaderScenarioGenerator
from CybORG.Agents import B_lineAgent
from CybORG.Agents import BlueReactRemoveAgent
from CybORG.Agents import BlueReactRestoreAgent
from CybORG.Agents import DroneRedAgent
from CybORG.Agents.Wrappers import RedTableWrapper
from CybORG.Agents.Wrappers.TrueTableWrapper import true_obs_to_table

path = "../CybORG/CybORG/Simulator/Scenarios/scenario_files/myscenario2.yaml"
sg = FileReaderScenarioGenerator(path)

blue_agent = BlueReactRemoveAgent()
red_agent = B_lineAgent()

env = CybORG(scenario_generator=sg, agents={'Blue':blue_agent, 'Red':red_agent})

results = env.reset(agent='Red')

pprint(env.get_ip_map())
for i in range(30):
    red_action_space = env.get_action_space('Red')
    red_obs = env.get_observation('Red')
    red_action = red_agent.get_action(observation=red_obs, action_space=red_action_space)

    results = env.step(action=red_action, agent='Red')

    print("--- STEP {} ---".format(1+i))
    print(red_action)
    pprint("Sucesso da ação: {}".format(red_obs.get('success')))
    print()
    if(red_action.name == "Impact"):
        break
