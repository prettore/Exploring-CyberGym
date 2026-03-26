import os
os.environ["PYTHONWARNINGS"] = "ignore"

from CybORG import CybORG
from VisualiseRedExpansionMod import VisualiseRedExpansionMod
from CybORG.Simulator.Scenarios import EnterpriseScenarioGenerator
from CybORG.Agents.Wrappers import EnterpriseMAE
from CybORG.Agents import SleepAgent, EnterpriseGreenAgent, FiniteStateRedAgent

from ray.rllib.algorithms.algorithm import Algorithm
from ray.tune.registry import register_env


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

mae = env_creator_CC4({})

print(help(mae.env))