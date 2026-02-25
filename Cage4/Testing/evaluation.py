from CybORG import CybORG
from CybORG.Simulator.Scenarios import EnterpriseScenarioGenerator
from CybORG.Agents.Wrappers import EnterpriseMAE
from CybORG.Agents import SleepAgent, EnterpriseGreenAgent, FiniteStateRedAgent

from ray.rllib.algorithms.algorithm import Algorithm
from ray.tune.registry import register_env

def env_creator_CC4(env_config: dict):

	sg = EnterpriseScenarioGenerator(
		blue_agent_class=SleepAgent,
		green_agent_class=EnterpriseGreenAgent,
		red_agent_class=FiniteStateRedAgent,
		steps=50
		)
	cyborg = CybORG(scenario_generator=sg)
	env = EnterpriseMAE(env=cyborg, agent_name="blue_agent") 

	return env

register_env(name="CC4", env_creator=lambda config: env_creator_CC4(config))
env = env_creator_CC4({})

NUM_AGENTS = 5
POLICY_MAP = {f"blue_agent_{i}": f"Agent{i}" for i in range(NUM_AGENTS)}

def policy_mapper(agent_id, episode, worker, **kwargs):
	return POLICY_MAP[agent_id]

results = env.reset()
from pprint import pprint
obs, _ = env.reset()

import os
base_dir = os.path.abspath(".")
checkpoint_path = os.path.join(base_dir, "results")
algo = Algorithm.from_checkpoint(checkpoint_path)

steps = 50
total = {}
for i in range(steps):

  actions = {}
  for agent_id, agent_obs in obs.items():
    ray_agent = POLICY_MAP[agent_id]
    actions[agent_id] = algo.compute_single_action(agent_obs, policy_id=ray_agent, explore=False)

  obs, rewards, dones, truncs, infos = env.step(actions)
  
  for agent_id, reward in rewards.items():
    if agent_id not in total:
      total[agent_id] = 0
    total[agent_id] += reward

pprint(total)