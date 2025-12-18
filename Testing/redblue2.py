from termcolor import colored
import sys
sys.path.append('/home/gabriel/Projects/CybORG-Sims/cage-challenge-2/CybORG/')
from pprint import pprint
tsize = 80

from CybORG import CybORG
from CybORG.Agents.SimpleAgents.B_line import *
from CybORG.Agents.SimpleAgents.BlueReactAgent import *
from CybORG.Shared.Actions.AbstractActions import Analyse

import inspect

path = str(inspect.getfile(CybORG))
path = path[:-10] + '/Shared/Scenarios/Scenario1b.yaml'

env = CybORG(path, 'sim')
# Qual é a diferença entre os dois??
# env = CybORG(scenario_gen)

results = env.reset(agent='Red')
obs = results.observation
# ou result = env.get_observation('Red')

action_space = results.action_space
print('')
# pprint(action_space)

red_obs = results.observation
agent = B_lineAgent()
blue = BlueReactRemoveAgent()

def step_red(obs, verbose=True):
    action = agent.get_action(obs, action_space)
    results = env.step(action=action, agent='Red')
    obs = results.observation

    if verbose:
        print(colored( f'{f"Red action: {action}":-^{tsize}}', 'red' ))
        pprint(obs)
        print('\n')
    return results

for i in range(30):
    print(colored(f'{f"ROUND {i+1}":*^{tsize}}', 'yellow'))
    print('\n')
    results = step_red(red_obs)
    red_obs = results.observation

    blue_obs = env.get_observation('Blue')
    print(colored(f'{"Blue observation":-^{tsize}}', 'blue'))
    pprint(blue_obs)
    print("\n")


host = env.get_last_action('Red').hostname

action = Analyse(session=0, agent='Blue', hostname=host) 

results = env.step(action=action, agent='Blue')

#print(colored(f'{"Blue Analyze":-^{tsize}}', 'blue'))
#pprint(results.observation)
#pprint(env.get_agent_state('Red'))

#cor = '\033[1;49;31m'
#print(colored(38*'-' + f'{"IP MAP": ^20}' + 38*'-', 'red'))
#pprint(env.get_ip_map())
