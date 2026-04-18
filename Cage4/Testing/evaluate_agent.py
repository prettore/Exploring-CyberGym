from CybORG import CybORG
from CybORG.Simulator.Scenarios import EnterpriseScenarioGenerator
from CybORG.Agents.Wrappers import EnterpriseMAE
from CybORG.Agents import SleepAgent, EnterpriseGreenAgent, FiniteStateRedAgent
from VisualiseRedExpansionMod import VisualiseRedExpansionMod

from ray.rllib.algorithms.algorithm import Algorithm
from ray.tune.registry import register_env

import networkx as nx
import sys
import argparse

# Function for crating EnterpriseMAE scenario
def env_creator_CC4(env_config: dict, max_steps=50):

	sg = EnterpriseScenarioGenerator(
		blue_agent_class=SleepAgent,
		green_agent_class=EnterpriseGreenAgent,
		red_agent_class=FiniteStateRedAgent,
		steps=max_steps
		)
	cyborg = CybORG(scenario_generator=sg)
	mae = EnterpriseMAE(env=cyborg, agent_name='blue_agent') 

	return mae

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("agent_path", type=str)
	parser.add_argument("--steps", type=int, default=50)
	args, _ = parser.parse_known_args()

	if True:
		agent_path = args.agent_path
		steps = args.steps

		register_env(name='CC4', env_creator=lambda config: env_creator_CC4(config, max_steps=steps))
		mae = env_creator_CC4({}, max_steps=steps)

		NUM_AGENTS = 5
		POLICY_MAP = {f'blue_agent_{i}': f'Agent{i}' for i in range(NUM_AGENTS)}

		def policy_mapper(agent_id, episode, worker, **kwargs):
			return POLICY_MAP[agent_id]

		#results = mae.reset()
		from pprint import pprint
		obs, _ = mae.reset()

		import os
		base_dir = os.path.abspath('.')

		# Retrieving the agent
		checkpoint_path = os.path.join(base_dir, agent_path)
		algo = Algorithm.from_checkpoint(checkpoint_path)

		total = {}
		reward_history = {agent_id: [] for agent_id in POLICY_MAP.keys()}

		visualise = VisualiseRedExpansionMod(mae.env, steps)

		for i in range(steps):

			# print(f"[DEBUG] Evaluation step {i}")

			actions = {}
			for agent_id, agent_obs in obs.items():
				ray_agent = POLICY_MAP[agent_id]
				actions[agent_id] = algo.compute_single_action(agent_obs, policy_id=ray_agent, explore=False)

			obs, rewards, dones, truncs, infos = mae.step(actions)
			
			for agent_id, reward in rewards.items():
				if agent_id not in total:
					total[agent_id] = 0
				
				total[agent_id] += reward

			for agent_id in POLICY_MAP.keys():
				reward_history[agent_id].append(total.get(agent_id, 0))

			visualise.modified_run(mae.env)

		import pickle

		#G[idx]['agent_label_mapping']
		collected_figures = visualise.get_figures()

		actions = visualise.all_actions

		script_dir = os.path.dirname(os.path.abspath(__file__))
		webgui_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'WebGUI_dash'))
		os.makedirs(webgui_dir, exist_ok=True)
		
		with open(os.path.join(webgui_dir, 'actions.pkl'), 'wb') as f:
			pickle.dump(actions, f)

		with open(os.path.join(webgui_dir, 'graph.pkl'), 'wb') as f:
			pickle.dump(collected_figures, f)

		with open(os.path.join(webgui_dir, 'rewards.pkl'), 'wb') as f:
			pickle.dump(reward_history, f)
	else:
		pass
		# print("[ERROR] Error on loading agent file - evaluate_agent.py")


main()