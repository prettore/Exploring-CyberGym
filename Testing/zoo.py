from CybORG import CybORG
from CybORG.Simulator.Scenarios import DroneSwarmScenarioGenerator
from CybORG.Agents.Wrappers.PettingZooParallelWrapper import PettingZooParallelWrapper

sg = DroneSwarmScenarioGenerator()

cyborg = CybORG(scenario_generator=sg)

agent_name = "blue_agent_0"

zoo_wrapped_cyborg = PettingZooParallelWrapper(env=cyborg)

obs = zoo_wrapped_cyborg.reset()

# obs são as observações iniciais em forma de dicionario
# obs.keys() são as chaves (agentes)
# print(obs.keys())
print("\n")
print(obs)

print("Vamos printar agora algumas cositas!\n")
observations, rewards, dones, infos = zoo_wrapped_cyborg.step({'blue_agent_0': 0, 'blue_agent_1': 0})

print(f"Observações: {observations}\nRecompensas: {rewards}\nConcluídos: {dones}\nInformações: {infos}\n")

# printa o vetor de observações do agente 0
# print(obs['blue_agent_0'])

action_space = zoo_wrapped_cyborg.action_space('blue_agent_0')
print(action_space)

actions = {k:action_space.sample() for k in obs}
obs, reward, done, info = zoo_wrapped_cyborg.step(actions)

print(f"Observações: {observations}\nRecompensas: {rewards}\nConcluídos: {dones}\nInformações: {infos}\n")
