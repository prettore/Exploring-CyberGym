from CybORG import CybORG
from CybORG.Agents import B_lineAgent
from CybORG.Agents.Wrappers import ChallengeWrapper

from ray.tune import register_env

def env_creator_CC1(env_config: dict):
    cyborg = CybORG(
        scenario_file="../cage-challenge-1/CybORG/CybORG/Shared/Scenarios/Scenario1b.yaml",
        steps=50
        )
    env = ChallengeWrapper(env=cyborg, agent_name="blue_agent")
    return env

register_env("CC1", env_creator=lambda config: env_creator_CC1(config))

config = {
    PPOConfig()
    .environment(env="CC1")
}

algo = config.build()

for _ in range(5):
    pprint(algo.train())

algo.save("./my_agent")