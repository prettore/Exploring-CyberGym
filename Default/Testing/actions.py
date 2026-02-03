import sys
sys.path.append('/home/gabriel/Projects/CybORG-Sims/CybORG')
import random
from os.path import dirname
from pprint import pprint

from CybORG import CybORG
from CybORG.Simulator.Scenarios import FileReaderScenarioGenerator


path = f'/home/gabriel/Projects/CybORG-Sims/CybORG/CybORG/Simulator/Scenarios/scenario_files/Scenario1b.yaml'
sg = FileReaderScenarioGenerator(path)
env = CybORG(scenario_generator=sg)

results = env.reset(agent='Red')
action_space = results.action_space

actions = action_space['action']

ips = action_space['ip_address']

import random
from CybORG.Simulator.Actions import DiscoverNetworkServices
unknown_ips = [ip for ip in ips if ips[ip]]
ip = random.choice(unknown_ips)

action = DiscoverNetworkServices(session=0,agent='Red',ip_address=ip)
results = env.step(action=action, agent='Red')

subnets = action_space['subnet']
known_subnets = [subnet for subnet in subnets if subnets[subnet]]
subnet = known_subnets[0]

pprint(subnets)
map = env.get_ip_map()
print('\n'+10*'-'+'\n')
pprint(map)



