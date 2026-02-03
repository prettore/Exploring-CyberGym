'''

This test is based on the simultaneous interaction between Red and Blue agents with the environment

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

class Simulation():
    def __init__(self, mode, agents, steps):
        pass
    def start():
        pass

path = '../Scenarios/Scenario1b.yaml'
scenario_gen = fr(path)

print('Modos')
print("0 - R vs R")
mode = int(input('Escolha o modo: '))

print('Agentes Vermelhos')
print('0 - Baseline')
print('1 - Meander')
num = int(input('Escolha o Agente V: '))
def select_red_agent():
    if num == 0:
        agent = B_lineAgent()
    elif num == 1:
        agent = RedMeanderAgent()
    return agent

red_agent = select_red_agent()

blue_agent = None
print('Agentes Azuis')
print('0 - React Remove')
print('1 - React Restore')
num = int(input('Escolha o Agente A: '))
def select_blue_agent():
    if num == 0:
        agent = BlueReactRemoveAgent()
    elif num == 1:
        agent = BlueReactRestoreAgent()
    return agent

blue_agent = select_blue_agent()

env = CybORG(scenario_gen) 

results = env.reset(agent='Red')

action_space = results.action_space
blue_action_space = env.get_action_space('Blue')
#green_action_space = env.get_action_space('Green')

red_obs = results.observation

def step_red(obs, verbose=True):
    action = red_agent.get_action(obs, action_space)
    results = env.step(action=action, agent='Red')

    if verbose:
        print(colored( f'{f"Red action: {action}": ^{tsize}}', 'red' ))
    return results

def step_blue(obs, verbose=True):
    action = blue_agent.get_action(obs, blue_action_space)
    results = env.step(action=action, agent='Blue')

    if verbose:
        print(colored( f'{f"Blue action: {action}": ^{tsize}}', 'blue' ))
        print('\n')
    return results

i = int(input("Digite o numero de iterações: "))

for i in range(i):
    print(colored(f'{f"ROUND {i+1}": ^{tsize}}', 'yellow'))
    results = step_red(red_obs)
    red_obs = results.observation
    print(colored(f'{"Red observation":-^{tsize}}', 'red' ))
    pprint(red_obs)
    #print(colored(f'{f"Sucesso: {red_obs["success"]}": ^{tsize}}', 'red'))
    print('\n')


    blue_obs = env.get_observation('Blue')
    print(colored(f'{"Blue observation":-^{tsize}}', 'blue'))
    pprint(blue_obs)
    results = step_blue(blue_obs)
    blue_obs = results.observation
    ##print(colored(f"Sucesso: {blue_obs["success"]}", 'blue'))
    print('\n')

'''
host = env.get_last_action('Red').hostname

action = Analyse(session=0, agent='Blue', hostname=host) 

results = env.step(action=action, agent='Blue')
'''
#print(colored(f'{"Blue Analyze":-^{tsize}}', 'blue'))
#pprint(results.observation)
#pprint(env.get_agent_state('Red'))

#cor = '\033[1;49;31m'
#print(colored(38*'-' + f'{"IP MAP": ^20}' + 38*'-', 'red'))
#pprint(env.get_ip_map())
