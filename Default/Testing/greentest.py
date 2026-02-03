'''

'''
from termcolor import colored
import sys
sys.path.append('/home/gabriel/Projects/CybORG-Sims/cage-challenge-2/CybORG/')
from pprint import pprint
tsize = 80

from CybORG import CybORG
from CybORG.Agents.SimpleAgents.B_line import *
from CybORG.Agents.SimpleAgents.Meander import *
from CybORG.Agents.SimpleAgents.BlueReactAgent import *
from CybORG.Agents.SimpleAgents.GreenAgent import *
#from CybORG.Shared.Actions.AbstractActions import Analyse
from CybORG.Simulator.Scenarios import FileReaderScenarioGenerator as fr

path = '../Scenarios/Scenario1b.yaml'
scenario_gen = fr(path)

agent = GreenAgent()

env = CybORG(scenario_gen) 

results = env.reset(agent='Green')

action_space = results.action_space

obs = results.observation

pprint(action_space)

allowed_ips = []
for key, value in action_space['ip_address'].items():
    if value == True:
        ip_str = key
        allowed_ips.append(ip_str)

print(allowed_ips)
