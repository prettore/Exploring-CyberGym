import sys
sys.path.append("../CybORG/")
from pprint import pprint

from CybORG import CybORG
from CybORG.Agents.SimpleAgents.B_line import B_lineAgent
from CybORG.Agents.SimpleAgents.BlueReactAgent import BlueReactRemoveAgent
from CybORG.Simulator.Scenarios import FileReaderScenarioGenerator as fr

path = "../Scenarios/Scenario1b.yaml"
scenario_gen = fr(path)

env = CybORG(scenario_gen, 'sim')

results = env.reset(agent='Red')

action_space = results.action_space
blue_action_space = env.get_action_space('Blue')

blue_agent = BlueReactRemoveAgent()
agent = B_lineAgent()
#agent = RedMeanderAgent()

red_obs = results.observation

for i in range(30):
   
    red_action = agent.get_action(red_obs, action_space)
    results = env.step(action=red_action, agent='Red')
    red_obs = results.observation

    print("--- RED ---")
    print(red_action)
    pprint("Sucesso da ação: {}".format(red_obs.get('success')))


    blue_obs = env.get_observation('Blue')
    blue_action = blue_agent.get_action(blue_obs, blue_action_space) 
    results = env.step(action=blue_action, agent='Blue')
    blue_obs = env.get_observation('Blue')
    
    print("--- BLUE ---")
    print(blue_action)
    pprint("Sucesso da ação: {}".format(blue_obs.get('success')))

    a = input("")
    print("\n\n")    
