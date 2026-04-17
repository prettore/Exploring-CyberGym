#import sys
#sys.path.append("../cage-challenge-4/")

from CybORG import CybORG
from CybORG.Simulator.Scenarios import EnterpriseScenarioGenerator
from CybORG.Agents.Wrappers import EnterpriseMAE
from CybORG.Agents import SleepAgent, EnterpriseGreenAgent, FiniteStateRedAgent

from ray.tune import register_env
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.algorithms.dqn import DQNConfig, DQN
from ray.rllib.policy.policy import PolicySpec

import networkx as nx
import matplotlib.pyplot as plt
import argparse
import os
import pickle
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("cage_name", type=str)
	parser.add_argument("--steps", type=int, default=1)
	parser.add_argument("--lr", type=float, default=0.0001)
	parser.add_argument("--batch_size", type=int, default=200)
	
	args, _ = parser.parse_known_args()
	
	if True:
		cage_name = args.cage_name
		steps_param = args.steps
		lr_param = args.lr
		batch_size_param = args.batch_size

		webgui_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'WebGUI_dash'))
		live_train_path = os.path.join(webgui_dir, 'live_train.pkl')
		live_metrics = {'steps': [], 'rewards': []}

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

		'''
		config = (
			PPOConfig()
			.environment(env="CC4")
			.framework("torch")
		)
		'''

		algo_config = (

			PPOConfig()

			.environment(env="CC4")

			.training(
				lr=lr_param, # learning rate
				# gamma=0.995, # discount factor
				# DQN -> e greedy?
				train_batch_size=batch_size_param
				)

			.debugging(logger_config={"logdir":"logs/PPO_Example", "type":"ray.tune.logger.TBXLogger"})

			.multi_agent(

			policies={

				ray_agent: PolicySpec(
					policy_class=None,
					observation_space=env.observation_space(cyborg_agent),
					action_space=env.action_space(cyborg_agent),
					config={"gamma": 0.85},
					) for cyborg_agent, ray_agent in POLICY_MAP.items()

					},
			policy_mapping_fn=policy_mapper

			)

			.env_runners(
				num_env_runners=1, 
				rollout_fragment_length=50, # optional
				# gym_env_vectorize_mode
				# num_cpus_per_env_runner
				# num_gpus_per_env_runner
				) 

		)

		algo = algo_config.build()

		for i in range(steps_param):
			
			# print(f"[DEBUG] Training step {i}")

			results = algo.train()
			
			live_metrics['steps'].append(i)
			mean_reward = results.get('episode_reward_mean')
			if mean_reward is None and 'env_runners' in results:
				mean_reward = results['env_runners'].get('episode_reward_mean', 0)
			if mean_reward is None:
				mean_reward = 0
				
			live_metrics['rewards'].append(mean_reward)
			with open(live_train_path, 'wb') as f:
				pickle.dump(live_metrics, f)

		root_path = 'results'

		# Creating root path (e.g. results_Cage4)
		root_path = os.path.join(root_path, cage_name)
		os.makedirs(root_path, exist_ok=True)
		# print(f"[DEBUG] Root path: {root_path}")

		# Creating list of current trainings on results_Cage4
		dirs = [f.name for f in os.scandir(root_path) if f.is_dir()]
		# print(f"[DEBUG] Directories: {dirs}")
		#max_dir = max(dirs, key=lambda file: file[-1])

		path = os.path.join(root_path, 'training')
		# print(f"[DEBUG] Path: {path}")
		if dirs == []:
			path += '1'
		else:
			max_dir_number = max([file[-1] for file in dirs])
			path += str(int(max_dir_number)+1)

		checkpoint_dir = algo.save(path)

		# print(f"[DEBUG] Checkpoint saved at: {checkpoint_dir.checkpoint.path}")


main()