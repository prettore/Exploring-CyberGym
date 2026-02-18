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

import matplotlib.pyplot as plt

def env_creator_CC4(env_config: dict):
    sg = EnterpriseScenarioGenerator(
        blue_agent_class=SleepAgent,
        green_agent_class=EnterpriseGreenAgent,
        red_agent_class=FiniteStateRedAgent,
        steps=50
        )
    cyborg = CybORG(scenario_generator=sg)
    state = cyborg.environment_controller.state
    G = state.link_diagram
    plt.savefig("scripts/graph.png")
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
    .rollouts(num_rollout_workers=1, rollout_fragment_length=50)
    .training(train_batch_size=200)
)

algo = algo_config.build()

for i in range(5):
    result = algo.train()

#checkpoint_dir = algo.save("results")
algo.save_to_path("./results")

#print("Checkpoint saved at:", checkpoint_dir.checkpoint.path)

