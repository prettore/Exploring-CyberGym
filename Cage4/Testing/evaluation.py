from ray.rllib.algorithms.algorithm import Algorithm
from ray.tune.registry import register_env
from CybORG import CybORG
from CybORG.Simulator.Scenarios import EnterpriseScenarioGenerator
from CybORG.Agents import SleepAgent, EnterpriseGreenAgent, FiniteStateRedAgent
from CybORG.Agents.Wrappers import EnterpriseMAE

# ---- SAME ENV CREATOR AS TRAINING ----
def env_creator_CC4(config):
    sg = EnterpriseScenarioGenerator(
        blue_agent_class=SleepAgent,
        green_agent_class=EnterpriseGreenAgent,
        red_agent_class=FiniteStateRedAgent,
        steps=20   # use a reasonable episode length
    )
    cyborg = CybORG(scenario_generator=sg)
    env = EnterpriseMAE(env=cyborg)
    return env

register_env(name="CC4", env_creator=lambda config: env_creator_CC4(config))

# ---- LOAD TRAINED MODEL ----
checkpoint_path = "/home/gabriel/Exploring-CyberGym/Cage4/Testing/results"
algo = Algorithm.from_checkpoint(checkpoint_path)

# ---- CREATE ENVIRONMENT ----
env = env_creator_CC4({})

episodes = 5
total_reward = 0

for ep in range(episodes):
    obs, info = env.reset()
    done = False
    ep_reward = 0

    while not done:
        action = algo.compute_single_action(obs, explore=False)  # no randomness
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        ep_reward += reward

    print(f"Episode {ep+1} reward: {ep_reward}")
    total_reward += ep_reward

print("Average reward:", total_reward / episodes)

