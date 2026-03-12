from CybORG import CybORG
from CybORG.Simulator.Scenarios import EnterpriseScenarioGenerator
from CybORG.Agents.Wrappers import EnterpriseMAE
from CybORG.Agents import SleepAgent, EnterpriseGreenAgent, FiniteStateRedAgent
from VisualiseRedExpansionMod import VisualiseRedExpansionMod

from ray.rllib.algorithms.algorithm import Algorithm
from ray.tune.registry import register_env

import networkx as nx
import sys

def env_creator_CC4(env_config: dict):

	sg = EnterpriseScenarioGenerator(
		blue_agent_class=SleepAgent,
		green_agent_class=EnterpriseGreenAgent,
		red_agent_class=FiniteStateRedAgent,
		steps=50
		)
	cyborg = CybORG(scenario_generator=sg)
	mae = EnterpriseMAE(env=cyborg, agent_name='blue_agent') 

	return mae

def main():
	if len(sys.argv) > 1:
		register_env(name='CC4', env_creator=lambda config: env_creator_CC4(config))
		mae = env_creator_CC4({})

		NUM_AGENTS = 5
		POLICY_MAP = {f'blue_agent_{i}': f'Agent{i}' for i in range(NUM_AGENTS)}

		def policy_mapper(agent_id, episode, worker, **kwargs):
			return POLICY_MAP[agent_id]

		#results = mae.reset()
		from pprint import pprint
		obs, _ = mae.reset()

		import os
		base_dir = os.path.abspath('.')

		agent_path = sys.argv[1]
		# Retrieving the agent
		checkpoint_path = os.path.join(base_dir, agent_path)
		algo = Algorithm.from_checkpoint(checkpoint_path)

		steps = 50
		total = {}

		visualise = VisualiseRedExpansionMod(mae.env, steps)

		for i in range(5):

			print('DEBUG')
			print('evaluation step', i)

			actions = {}
			for agent_id, agent_obs in obs.items():
				ray_agent = POLICY_MAP[agent_id]
				actions[agent_id] = algo.compute_single_action(agent_obs, policy_id=ray_agent, explore=False)

			obs, rewards, dones, truncs, infos = mae.step(actions)
			
			for agent_id, reward in rewards.items():
				if agent_id not in total:
					total[agent_id] = 0
				
				total[agent_id] += reward

			visualise.modified_run(mae.env)

		import pickle

		#G[idx]['agent_label_mapping']
		collected_figures = visualise.get_figures()

		with open('graph.pkl', 'wb') as f:
			pickle.dump(collected_figures, f)

		# TODO - CRIAR VISUALIZAÇÃO DE RECOMPENSAS
		# pprint(total)
	else:
		print('Error on loading agent file - evaluate_agent.py')

if __name__ == '__main__':
	main()