import re
import json

from CybORG import CybORG
from CybORG.Simulator.Scenarios import EnterpriseScenarioGenerator
from CybORG.Agents.Wrappers import EnterpriseMAE
from CybORG.Agents import SleepAgent, EnterpriseGreenAgent, FiniteStateRedAgent

from ray.tune import register_env
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.policy.policy import PolicySpec

import argparse
import os

def main():
	# Adding arguments to be able to train the agent from the terminal
	parser = argparse.ArgumentParser()
	parser.add_argument("cage_name", type=str)
	parser.add_argument("--steps", type=int, default=1)
	parser.add_argument("--lr", type=float, default=0.0001)
	parser.add_argument("--batch_size", type=int, default=200)

	args, _ = parser.parse_known_args()

	cage_name = args.cage_name
	steps_param = args.steps
	lr_param = args.lr
	batch_size_param = args.batch_size

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

	algo_config = (
		PPOConfig()
		.environment(env="CC4")
		.training(
			lr=lr_param,           # learning rate
			# gamma=0.995,         # discount factor
			train_batch_size=batch_size_param
			)
		.debugging(logger_config={"logdir": "logs/PPO_Example", "type": "ray.tune.logger.TBXLogger"})
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
			rollout_fragment_length=50,  # optional
			# num_cpus_per_env_runner=1,
			# num_gpus_per_env_runner=0,
		)
	)

	algo = algo_config.build()

	webgui_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'WebGUI_dash'))
	live_train_path = os.path.join(webgui_dir, 'live_train.json')
	live_data = []
	# Start fresh each run
	with open(live_train_path, 'w') as lf:
		json.dump(live_data, lf)

	for i in range(steps_param):
		results = algo.train()

		# Defensive: episode_reward_mean, min, max location varies across Ray versions
		mean_reward = results.get('episode_reward_mean')
		if mean_reward is None and 'env_runners' in results:
			mean_reward = results['env_runners'].get('episode_reward_mean', 0)
		if mean_reward is None:
			mean_reward = 0

		min_reward = results.get('episode_reward_min')
		if min_reward is None and 'env_runners' in results:
			min_reward = results['env_runners'].get('episode_reward_min', 0)
		if min_reward is None:
			min_reward = 0

		max_reward = results.get('episode_reward_max')
		if max_reward is None and 'env_runners' in results:
			max_reward = results['env_runners'].get('episode_reward_max', 0)
		if max_reward is None:
			max_reward = 0

		# Stream metric to dashboard
		live_data.append({
			'step': i, 
			'reward': float(mean_reward),
			'reward_mean': float(mean_reward),
			'reward_min': float(min_reward),
			'reward_max': float(max_reward)
		})
		with open(live_train_path, 'w') as lf:
			json.dump(live_data, lf)

	# Save checkpoint --------------------------------------------------------
	root_path = os.path.join('results', cage_name)
	os.makedirs(root_path, exist_ok=True)

	dirs = [f.name for f in os.scandir(root_path) if f.is_dir()]

	if not dirs:
		next_number = 1
	else:
		# Parse the trailing integer from each directory name so that
		# training10 sorts correctly after training9 (was: file[-1] → '0').
		nums = []
		for d in dirs:
			m = re.search(r'(\d+)$', d)
			if m:
				nums.append(int(m.group(1)))
		next_number = max(nums) + 1 if nums else 1

	path = os.path.join(root_path, f'training{next_number}')
	algo.save(path)


main()