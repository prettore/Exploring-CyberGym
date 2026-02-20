from CybORG import CybORG
from CybORG.Agents import B_lineAgent
from CybORG.Agents.Wrappers import ChallengeWrapper

from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.policy.policy import PolicySpec
from ray.tune import register_env

cyborg = CybORG(
        scenario_file="../cage-challenge-1/CybORG/CybORG/Shared/Scenarios/Scenario1b.yaml",
        seed=1
        )

env = cyborg

obs = env.reset()

done = False

action_space = env.get_action_space()

print("Cage1 working")