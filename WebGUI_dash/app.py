import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import networkx as nx
import plotly.graph_objs as go
import random
import pandas as pd

import subprocess

cages = ('Cage1', 'Cage2', 'Cage3', 'Cage4')

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def start_training(cage_path):
    python_exec = os.path.join(BASE_DIR, '..', cage_path, '.venv', 'bin', 'python')
    script_path = os.path.join(BASE_DIR, '..', cage_path, 'Testing', 'train.py')

    env = os.environ.copy()
    env['PYTHONPATH'] = '/home/gabriel/Exploring-CyberGym/Cage4/cage-challenge-4'

    return subprocess.Popen(
        [python_exec, script_path],
      env=env
    )

import requests, pickle

def evaluate_agent(cage_path, agent_path):
    # TODO - Create a way to choose the agent file
    agent_path = 'evaluate_agent.py'
    python_exec = os.path.join(BASE_DIR, '..', cage_path, '.venv', 'bin', 'python')
    script_path = os.path.join(BASE_DIR, '..', cage_path, 'Testing', agent_path)

    env = os.environ.copy()
    env['PYTHONPATH'] = '/home/gabriel/Exploring-CyberGym/Cage4/cage-challenge-4'

    return subprocess.Popen(
       [python_exec, script_path],
      env=env
    )

def create_graph(idx):
    
    collected_figures = None
    try:
        with open('graph.pkl', 'rb') as f:
           collected_figures = pickle.load(f)
    except FileNotFoundError:
        print('File not found!')
        return None

    fig = collected_figures[idx]
    print(collected_figures[1])
    return fig

    
'''
def create_graph():
    G = nx.erdos_renyi_graph(n=20, p=0.2)

    # Adicionar peso ou atributo exemplo
    for node in G.nodes():
        G.nodes[node]['value'] = random.randint(1, 100)

    return G
'''

# =========================
# App Dash
# =========================
app = dash.Dash(__name__)

app.layout = html.Div([

    html.H2('Choose Cage'),

    dcc.Dropdown(
        cages,
        'cage-challenge-1',
        id='choose-cage'
    ),

    html.Div(id="train-loading"),

    html.P(id='train-warning'),

    dcc.Button('Train', id='train', n_clicks=0),

    dcc.Dropdown(
        'agent',
        'cage-challenge-1',
        id='choose-agent'
    ),

    html.Div(id="eval-loading"),

    html.P(id='eval-warning'),

    dcc.Button('Evaluate', id='eval', n_clicks=0),

    html.P(id='dummy'),

    dcc.Store(id='cage-path', data='None'),

    dcc.Store(id="train-running"),

    dcc.Store(id="eval-running"),
    
    dcc.Interval(
        id="train-poller",
        interval=1000,
        disabled=True
    ),

    dcc.Interval(
        id="eval-poller",
        interval=1000,
        disabled=True
    ),

    dcc.Interval(
    id="train-warning-clear",
    interval=2000,
    n_intervals=0,
    disabled=True
    ),

    dcc.Interval(
    id="eval-warning-clear",
    interval=2000,
    n_intervals=0,
    disabled=True
)

]), html.Div([

    html.H2('Rede Interativa'),

    dcc.Graph(
        id='network-graph',
        figure={
            'data': [],
            'layout': {}
        },
        style={'height': '80vh',
        'display': 'none'}
        ),

    dcc.Button('>', id='start'),  # Ao apertar o botão, o Slider será movimentado automaticamente!

    dcc.Button('||', id='pause'), # pausa!

    html.Div(

    id='slider-container',
    children=[
        dcc.Slider(
            0,
            5,
            value=0,
            id='network-slider'
            )
    ],
    style={'display': 'none'}  # esconde aqui

    ),

]), html.Footer([

    html.H5('This is a scientific initiation project that uses CybORG research gym')

])

@app.callback(
    Output('network-graph', 'figure', allow_duplicate=True),
    Input('network-slider', 'value'),
    prevent_initial_call=True
)
def update_graph(value):
    fig = create_graph(value)
    return fig

# Callback for checking if the training is complete
@app.callback(
    Output('train-loading', 'children'),
    Output('train-poller', 'disabled', allow_duplicate=True),
    Input('train-poller', 'n_intervals'),
    State('train-running', 'data'),
    prevent_initial_call=True
)
def check_train(n, running):
    global train_process

    if not running:
        return '', True

    if train_process.poll() is None:
        return 'Training...', False

    return 'Finished!', True

train_process = None

@app.callback(
    Output('train-warning', 'children', allow_duplicate=True),
    Output('train-warning-clear', 'disabled'),
    Input('train-warning-clear', 'n_intervals')
)
def clean_warning(n):
    return '', True

@app.callback(
    Output('train-warning', 'children', allow_duplicate=True),
    Output('train-warning-clear', 'disabled'),
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
    if train_process:
        return 'Already training!', True, False, True
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
    Output('eval-poller', 'disabled', allow_duplicate=True),
    Output('eval-running', 'data'),
    Output('network-graph', 'style', allow_duplicate=True),
    Output('slider-container', 'style', allow_duplicate=True),
    Input('eval', 'n_clicks'),
    State('cage-path', 'data'),
    prevent_initial_call=True
)
def eval(n_clicks, data):

    global eval_process
    # If it is already training, do nothing
    if eval_process:
        return 'Already evaluating!', False, True, {'display': 'none'}, {'display': 'none'}
    eval_process = evaluate_agent(data, '')
    # TODO - Create a way to acess trained agent and choose them

    return '', False, True, {'display': 'block'}, {'display': 'block'}

@app.callback(
    Output('cage-path', 'data'),
    Input('choose-cage', 'value'),
    prevent_initial_call=True
)
def choose_cage(value):
    return value

if __name__ == '__main__':
    app.run(debug=True)
