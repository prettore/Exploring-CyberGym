import os
from CybORG import CybORG
from CybORG.Agents.SimpleAgents.KeyboardAgent import KeyboardAgent

def main():
    """
    Script para interagir com o ambiente CybORG usando o KeyboardAgent.
    """
    # Descobre o diretório onde este script está rodando (.../Cage4/Testing)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Volta duas pastas e entra em 'Scenarios'
    scenarios_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'Scenarios'))
    
    if not os.path.exists(scenarios_dir):
        print(f"Erro: A pasta de cenários não foi encontrada em {scenarios_dir}")
        return

    # Lista os arquivos de cenário disponíveis
    available_scenarios = [f for f in os.listdir(scenarios_dir) if f.endswith('.yaml')]
    
    if not available_scenarios:
        print(f"Nenhum arquivo .yaml encontrado na pasta {scenarios_dir}")
        return

    # Deixa o usuário escolher o cenário
    print("Cenários disponíveis:")
    for i, scenario in enumerate(available_scenarios):
        print(f"[{i}] {scenario}")
        
    try:
        escolha = int(input("\nDigite o número do cenário que deseja jogar: "))
        scenario_file = available_scenarios[escolha]
    except (ValueError, IndexError):
        print("Escolha inválida. Execução cancelada.")
        return

    scenario_path = os.path.join(scenarios_dir, scenario_file)
    print(f"\nInicializando o ambiente CybORG...\nCaminho: {scenario_path}")
    
    try:
        env = CybORG(scenario_path, 'sim')
    except Exception as e:
        print(f"Erro ao inicializar o cenário: {e}")
        return

    # Deixa o usuário escolher o lado
    escolha_agente = input("Deseja jogar como Blue (Defesa) ou Red (Ataque)? [B/r]: ").strip().lower()
    agent_name = 'Red' if escolha_agente == 'r' else 'Blue'
    
    agent = KeyboardAgent()

    print(f"\n[{agent_name}] Jogo iniciado! Você tem 50 passos para agir.")
    
    results = env.reset(agent_name)
    obs = results.observation
    action_space = results.action_space
    
    step = 0
    max_steps = 50 # Limite de passos por episódio

    while step < max_steps:
        print(f"\n{'='*20} Passo {step} {'='*20}")
        
        # O KeyboardAgent irá solicitar que você digite a ação no terminal
        action = agent.get_action(obs, action_space)
        
        # Executa a ação no ambiente
        results = env.step(agent=agent_name, action=action)
        
        obs = results.observation
        action_space = results.action_space
        reward = results.reward
        done = results.done
        
        print(f"Recompensa obtida neste passo: {reward}")
        
        if done:
            print("\n[!] O episódio terminou. Reiniciando o ambiente...")
            results = env.reset(agent_name)
            obs = results.observation
            action_space = results.action_space
            step = 0
        else:
            step += 1
            
    print("Limite de passos atingido. Encerrando o jogo.")

if __name__ == "__main__":
    main()
