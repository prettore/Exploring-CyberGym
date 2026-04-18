import os
import shutil
import subprocess
import pickle
import time
from functools import lru_cache
from typing import Dict, List, Optional, Any
import plotly.graph_objs as go

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Global cache for performance
_cached_data = {
    'graphs': None,
    'actions': None,
    'rewards': None,
    'reward_figure': None,
    'last_load_time': 0
}

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
def evaluate_agent(cage_path, agent_path, steps):
    root_path = 'results'
    agent_path = os.path.join(root_path, cage_path, agent_path)

    # print(f"[DEBUG] Evaluating agent path: {agent_path}")

    python_exec = os.path.join(BASE_DIR, '..', cage_path, '.venv', 'bin', 'python')
    script_path = os.path.join(BASE_DIR, '..', cage_path, 'Testing', 'evaluate_agent.py')

    env = os.environ.copy()
    challenge_dir = f'cage-challenge-{cage_path[-1]}'
    env['PYTHONPATH'] = os.path.abspath(os.path.join(BASE_DIR, '..', cage_path, challenge_dir))

    args = [
        python_exec, script_path, 
        agent_path, 
        "--steps", str(steps)
    ]

    return subprocess.Popen(args, env=env)

# Retrieve graph from 'collected_figures' with caching
def create_graph(idx):
    global _cached_data
    
    # Load data if not cached or cache is stale
    if _cached_data['graphs'] is None:
        try:
            with open(os.path.join(BASE_DIR, 'graph.pkl'), 'rb') as f:
               _cached_data['graphs'] = pickle.load(f)
        except FileNotFoundError:
            return None
    
    # Return cached graph
    if idx < len(_cached_data['graphs']):
        return _cached_data['graphs'][idx]
    return None

def get_actions():
    global _cached_data
    
    # Load data if not cached
    if _cached_data['actions'] is None:
        try:
            with open(os.path.join(BASE_DIR, 'actions.pkl'), 'rb') as f:
               _cached_data['actions'] = pickle.load(f)
        except FileNotFoundError:
            return None
    
    return _cached_data['actions']

def get_rewards():
    global _cached_data
    
    # Load data if not cached
    if _cached_data['rewards'] is None:
        try:
            with open(os.path.join(BASE_DIR, 'rewards.pkl'), 'rb') as f:
               _cached_data['rewards'] = pickle.load(f)
        except FileNotFoundError:
            return None
    
    return _cached_data['rewards']

def get_live_metrics():
    metrics = None
    try:
        with open(os.path.join(BASE_DIR, 'live_train.pkl'), 'rb') as f:
           metrics = pickle.load(f)
    except FileNotFoundError:
        return None

    return metrics

# Create optimized reward figure with caching
def create_reward_figure(current_step=None):
    global _cached_data
    
    rewards = get_rewards()
    if not rewards:
        return go.Figure()
    
    # Create figure if not cached
    if _cached_data['reward_figure'] is None:
        fig = go.Figure()
        
        for agent_id, history in rewards.items():
            fig.add_trace(go.Scatter(
                x=list(range(len(history))),
                y=history,
                mode='lines+markers',
                name=agent_id,
                line=dict(width=2)
            ))
        
        fig.update_layout(
            title="Cumulative Rewards",
            xaxis_title="Step",
            yaxis_title="Reward",
            margin=dict(l=40, r=40, t=40, b=40),
            template="plotly_white",
            hovermode="x unified"
        )
        
        _cached_data['reward_figure'] = fig
    
    # Add vertical line if step is specified
    if current_step is not None:
        fig_copy = go.Figure(_cached_data['reward_figure'])
        fig_copy.add_vline(x=current_step, line_dash="dash", line_color="black", line_width=2)
        return fig_copy
    
    return _cached_data['reward_figure']

# Clear cache when new evaluation starts
def clear_cache():
    global _cached_data
    _cached_data = {
        'graphs': None,
        'actions': None,
        'rewards': None,
        'reward_figure': None,
        'last_load_time': 0
    }
