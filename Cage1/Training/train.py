# Adding cage to system path
import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAGE_ROOT = os.path.join(BASE_DIR, "..", "cage-challenge-1")
sys.path.insert(0, CAGE_ROOT)

from CybORG import CybORG
from CybORG.Agents import B_lineAgent
from CybORG.Agents.Wrappers import ChallengeWrapper

from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.policy.policy import PolicySpec
from ray.tune import register_env

def env_creator_CC1(env_config: dict):
    cyborg = CybORG(
        scenario_file="../cage-challenge-1/CybORG/CybORG/Shared/Scenarios/Scenario1b.yaml"
        )
    env = ChallengeWrapper(env=cyborg, agent_name="Blue")
    return env

register_env("CC1", env_creator=lambda config: env_creator_CC1(config))

def policy_mapper(agent_id, episode, worker, **kwargs):
    return POLICY_MAP[agent_id]

config = (
    PPOConfig()
    .environment(env="CC1")
)

algo = config.build()

for _ in range(5):
    result = algo.train()

algo.save("./my_agent")