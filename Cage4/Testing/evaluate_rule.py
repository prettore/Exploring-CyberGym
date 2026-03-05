from CybORG import CybORG
from CybORG.Simulator.Scenarios import EnterpriseScenarioGenerator
from CybORG.Agents import SleepAgent, EnterpriseGreenAgent, FiniteStateRedAgent
from CybORG.Agents.Wrappers.TrueStateWrapper import TrueStateTableWrapper
from CybORG.Agents.Wrappers.VisualiseRedExpansion import VisualiseRedExpansion
from CybORG.Agents.Wrappers import EnterpriseMAE

from ray.tune import register_env
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.policy.policy import PolicySpec


from ray.rllib.algorithms.algorithm import Algorithm
import os
from agent import SmartBlueAgent

steps=10
sg = EnterpriseScenarioGenerator(
    blue_agent_class=SleepAgent,
	green_agent_class=EnterpriseGreenAgent,
	red_agent_class=FiniteStateRedAgent,
	steps=steps
)

cyborg = CybORG(scenario_generator=sg, seed=1234)

visualise = VisualiseRedExpansion(cyborg, steps)
visualise.run()

#env = TrueStateTableWrapper(cyborg)
#results = cyborg.reset()
#env.print_host_overview_table()