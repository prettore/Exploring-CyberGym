import sys
sys.path.append('../CybORG')
from CybORG import CybORG
from CybORG.Simulator.Scenarios import FileReaderScenarioGenerator
from CybORG.Agents import *
from CybORG.Simulator.Actions import *
from CybORG.Agents.Wrappers import RedTableWrapper

path = f'../CybORG/CybORG/Simulator/Scenarios/scenario_files/Scenario1b.yaml'
sg = FileReaderScenarioGenerator(path)

cyborg = CybORG(sg,agents={'Blue':MonitorAgent()})
env = RedTableWrapper(env=cyborg, output_mode='table')

agent = KeyboardAgent()

results = env.reset('Red')
obs = results.observation
action_space = results.action_space

while True:
    print(obs)
    action = agent.get_action(obs,action_space)
    results = env.step(action=action,agent='Red')
    results2 = cyborg.step(action=action,agent='Red')
    obs = env.get_observation('Red')
    obs2 = results2.observation
    if (env.get_last_action('Red').__class__.__name__ == 'Impact') and (obs2['success'] == 'TRUE'):
        break;
