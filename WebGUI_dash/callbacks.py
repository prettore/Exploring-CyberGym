from dash.dependencies import Input, Output, State
from dash import html, dcc
import plotly.graph_objs as go
from app import app
import subprocess


# Retrieving current dir
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Listing possible environments
CAGES = ('Cage4')

# Listing trained agent files
def list_trained_agents(cage_path):

    if cage_path == None:
        return None
    import os
	
    root_path = "results"
    root_path = os.path.join(root_path, cage_path)
    #path = os.path.join(root_path, 'training')

    os.makedirs(root_path, exist_ok=True)

    agent_files = [f.name for f in os.scandir(root_path) if f.is_dir()]
    return agent_files

import shutil
def delete_files_on_startup():
    
    for cage in CAGES:
        root_path = 'results'
        root_path = os.path.join(root_path, cage)

        for dir_name in os.listdir(root_path):
            dir_path = os.path.join(BASE_DIR, root_path, dir_name)
            if os.path.isdir(dir_path):
                try:
                    shutil.rmtree(dir_path)
                except OSError as e:
                    print(f'Error on deleting File: {e}')
        
# Create train_agent.py subprocess
def start_training(cage_path):
    # Specifying python path enables usage of the specific
    python_exec = os.path.join(BASE_DIR, '..', cage_path, '.venv', 'bin', 'python')
    script_path = os.path.join(BASE_DIR, '..', cage_path, 'Testing', 'train_agent.py')

    # Insert cage on python path, for it isn't a pip package
    env = os.environ.copy()
    env['PYTHONPATH'] = '/home/gabriel/Exploring-CyberGym/Cage4/cage-challenge-4'

    return subprocess.Popen(
        [python_exec, script_path, cage_path],
      env=env
    )

import requests, pickle
# Create evaulate_agent.py subprocess
def evaluate_agent(cage_path, agent_path):
    root_path = 'results'
    agent_path = os.path.join(root_path, cage_path, agent_path)

    print(agent_path)

    python_exec = os.path.join(BASE_DIR, '..', cage_path, '.venv', 'bin', 'python')
    script_path = os.path.join(BASE_DIR, '..', cage_path, 'Testing', 'evaluate_agent.py')
    # TODO - Create a way to choose the agent file

    env = os.environ.copy()
    env['PYTHONPATH'] = '/home/gabriel/Exploring-CyberGym/Cage4/cage-challenge-4'

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
        print('File not found!')
        return None

    fig = collected_figures[idx]
    #print(collected_figures[1])
    return fig

def get_actions():
    actions = {}
    try:
        with open(os.path.join(BASE_DIR, 'actions.pkl'), 'rb') as f:
           actions = pickle.load(f)
    except FileNotFoundError:
        print('File not found!')
        return None

    return actions

@app.callback(
    Output('cage-path', 'data'),
    Input('choose-cage', 'value'),
)
def choose_cage(cage):
    #AGENT_FILES = list_trained_agents(cage)
    return cage

@app.callback(
    Output('agent-path', 'data'),
    Input('choose-agent', 'value'),
    prevent_initial_call=True
)
def choose_agent(agent):
    return agent

from pprint import pprint
@app.callback(
    Output('network-graph', 'figure', allow_duplicate=True),
    Output('actions', 'children'),
    Input('network-slider', 'value'),
    prevent_initial_call=True
)
def update_graph(value):
    fig = create_graph(value)

    all_actions = get_actions()
    actions = all_actions[value]

    return fig, html.Div([
        html.Div(f"{agent}: {action}") for agent, action in actions.items()
    ]) 

# Callback for checking if the training is complete
@app.callback(
    Output('train-loading', 'children'),
    Output('train-poller', 'disabled', allow_duplicate=True),
    Output('choose-agent','options'),
    Input('train-poller', 'n_intervals'),
    State('train-running', 'data'),
    State('cage-path', 'data'),
    prevent_initial_call=True
)
def check_train(n, running, cage):
    global train_process

    if not running:
        return '', True

    if train_process.poll() is None:
        agent_files = list_trained_agents(cage)
        return 'Training...', False, agent_files

    agent_files = list_trained_agents(cage)
    return 'Finished!', True, agent_files

train_process = None

@app.callback(
    Output('train-warning', 'children', allow_duplicate=True),
    Output('train-warning-clear', 'disabled'),
    Input('train-warning-clear', 'n_intervals'),
    prevent_initial_call=True
)
def clean_train_warning(n):
    return '', True

@app.callback(
    Output('train-warning', 'children', allow_duplicate=True),
    Output('train-warning-clear', 'disabled', allow_duplicate=True),
    Output('train-poller', 'disabled', allow_duplicate=True),
    Output('train-running', 'data'),
    Input('train', 'n_clicks'),
    State('cage-path', 'data'),
    prevent_initial_call=True
)
def train(n_clicks, data):

    if data == None:
        return 'Choose a Cage first!', False, True, False
    
    global train_process
    # If it is already training, do nothing
    if train_process and train_process.poll() is None:
        return 'Already training!', False, False, True
    train_process = start_training(data)
    return '', True, False, True

# TODO - Create evaluation
# Callback for checking if the evaluation is complete
@app.callback(
    Output('eval-loading', 'children'),
    Output('eval-poller', 'disabled', allow_duplicate=True),
    Input('eval-poller', 'n_intervals'),
    State('eval-running', 'data'),
    prevent_initial_call=True
)
def check_eval(n, running):
    global eval_process

    if not running:
        return '', True

    if eval_process.poll() is None:
        return 'Evaluating...', False

    return 'Finished!', True

eval_process = None

@app.callback(
    Output('eval-warning', 'children', allow_duplicate=True),
    Output('eval-warning-clear', 'disabled', allow_duplicate=True),
    Output('eval-poller', 'disabled', allow_duplicate=True),
    Output('eval-running', 'data'),
    Output('network-graph', 'style', allow_duplicate=True),
    Output('slider-container', 'style', allow_duplicate=True),
    Input('eval', 'n_clicks'),
    State('cage-path', 'data'),
    State('agent-path','data'),
    prevent_initial_call=True
)
def eval(n_clicks, cage, agent):

    if agent == None:
        return 'Choose an agent first!', False, False, False, {'display': 'none'}, {'display': 'none'}

    global eval_process
    # If it is already training, do nothing
    if eval_process and eval_process.poll() is None:
        return 'Already evaluating!', False, False, True, {'display': 'none'}, {'display': 'none'}
    eval_process = evaluate_agent(cage, agent)

    return '', True, False, True, {'display': 'block'}, {'display': 'block'}

@app.callback(
    Output('eval-warning', 'children', allow_duplicate=True),
    Output('eval-warning-clear', 'disabled'),
    Input('eval-warning-clear', 'n_intervals'),
    prevent_initial_call=True
)
def clean_eval_warning(n):
    return '', True

@app.callback(
    Output('choose-agent', 'options', allow_duplicate=True),
    Input('choose-cage', 'value'),
    prevent_initial_call=True
)
def update_agent_dropdown(cage):
    if cage is None:
        return []

    agent_files = list_trained_agents(cage)
    return agent_files