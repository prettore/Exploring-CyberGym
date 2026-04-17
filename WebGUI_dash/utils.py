import os
import shutil
import subprocess
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Listing possible environments
CAGES = ('Cage4',)

# Listing trained agent files
def list_trained_agents(cage_path):
    if cage_path == None:
        return None
    root_path = "results"
    root_path = os.path.join(root_path, cage_path)

    os.makedirs(root_path, exist_ok=True)
    agent_files = [f.name for f in os.scandir(root_path) if f.is_dir()]
    return agent_files

def delete_files_on_startup():
    live_train_path = os.path.join(BASE_DIR, 'live_train.pkl')
    if os.path.isfile(live_train_path):
        os.remove(live_train_path)

    for cage in CAGES:
        root_path = 'results'
        root_path = os.path.join(root_path, cage)

        for dir_name in os.listdir(root_path):
            dir_path = os.path.join(BASE_DIR, root_path, dir_name)
            if os.path.isdir(dir_path):
                try:
                    shutil.rmtree(dir_path)
                except OSError as e:
                    # print(f"[ERROR] Error on deleting File: {e}")
                    pass
        
# Create train_agent.py subprocess
def start_training(cage_path, steps=1, lr=0.0001, batch_size=200):
    # Specifying python path enables usage of the specific
    python_exec = os.path.join(BASE_DIR, '..', cage_path, '.venv', 'bin', 'python')
    script_path = os.path.join(BASE_DIR, '..', cage_path, 'Testing', 'train_agent.py')

    # Insert cage on python path, for it isn't a pip package
    env = os.environ.copy()
    challenge_dir = f'cage-challenge-{cage_path[-1]}' # e.g. cage-challenge-4
    env['PYTHONPATH'] = os.path.abspath(os.path.join(BASE_DIR, '..', cage_path, challenge_dir))

    args = [
        python_exec, script_path, 
        cage_path, 
        "--steps", str(steps), 
        "--lr", str(lr), 
        "--batch_size", str(batch_size)
    ]

    return subprocess.Popen(args, env=env)

# Create evaluate_agent.py subprocess
def evaluate_agent(cage_path, agent_path):
    root_path = 'results'
    agent_path = os.path.join(root_path, cage_path, agent_path)

    # print(f"[DEBUG] Evaluating agent path: {agent_path}")

    python_exec = os.path.join(BASE_DIR, '..', cage_path, '.venv', 'bin', 'python')
    script_path = os.path.join(BASE_DIR, '..', cage_path, 'Testing', 'evaluate_agent.py')

    env = os.environ.copy()
    challenge_dir = f'cage-challenge-{cage_path[-1]}'
    env['PYTHONPATH'] = os.path.abspath(os.path.join(BASE_DIR, '..', cage_path, challenge_dir))

    return subprocess.Popen(
       [python_exec, script_path, agent_path],
      env=env
    )

# Retrieve graph from 'collected_figures'
def create_graph(idx):
    collected_figures = None
    try:
        with open(os.path.join(BASE_DIR, 'graph.pkl'), 'rb') as f:
           collected_figures = pickle.load(f)
    except FileNotFoundError:
        # print("[ERROR] Graph File not found!")
        return None

    fig = collected_figures[idx]
    return fig

def get_actions():
    actions = {}
    try:
        with open(os.path.join(BASE_DIR, 'actions.pkl'), 'rb') as f:
           actions = pickle.load(f)
    except FileNotFoundError:
        # print("[ERROR] Actions File not found!")
        return None

    return actions

def get_rewards():
    rewards = {}
    try:
        with open(os.path.join(BASE_DIR, 'rewards.pkl'), 'rb') as f:
           rewards = pickle.load(f)
    except FileNotFoundError:
        # print("[ERROR] Rewards file not found!")
        return None

    return rewards

def get_live_metrics():
    metrics = None
    try:
        with open(os.path.join(BASE_DIR, 'live_train.pkl'), 'rb') as f:
           metrics = pickle.load(f)
    except FileNotFoundError:
        return None

    return metrics
