from CybORG import CybORG
from CybORG.Agents.SimpleAgents.BaseAgent import BaseAgent
from CybORG.Shared import Results
from ray.tune import register_env
from CybORG.Simulator.Scenarios import EnterpriseScenarioGenerator
from CybORG.Agents import SleepAgent, EnterpriseGreenAgent, FiniteStateRedAgent
from CybORG.Agents.Wrappers import EnterpriseMAE


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

class SmartBlueAgent(BaseAgent):
        def __init__(self, algo, agent_id):
                self.algo = algo
                self.agent_id = agent_id
                self.mae = env_creator_CC4({})
                self.last_obs = self.mae.reset()

        def get_action(self, observation, action_space=None):

                action_index = self.algo.compute_single_action(self.last_obs, policy_id=self.agent_id)
                print("Ação MAE")
                print(action_index)
                cyborg_action = self.mae.action_space(agent_name).actions[action_index]
                print("Ação CYBORG")
                print(cyborg_action)
                # step MAE env to keep it synchronized
                self.last_obs, _, _, _, _ = self.mae.step({self.policy_id: action_index})

                # precisa converter action do MAE para cyborg!
                return cyborg_action
        def end_episode(self):
                pass
        def set_initial_values(self, action_space, observation):
                pass
        def train(self, results: Results):
                pass