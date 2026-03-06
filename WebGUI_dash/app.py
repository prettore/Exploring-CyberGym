import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import networkx as nx
import plotly.graph_objs as go
import random
import pandas as pd

import subprocess

cages = ("Cage1", "Cage2", "Cage3", "Cage4")

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def start_training(cage_path):
    python_exec = os.path.join(BASE_DIR, "..", cage_path, ".venv", "bin", "python")
    script_path = os.path.join(BASE_DIR, "..", cage_path, "Testing", "train.py")

    env = os.environ.copy()
    env["PYTHONPATH"] = "/home/gabriel/Exploring-CyberGym/Cage4/cage-challenge-4"

    subprocess.Popen(
        [python_exec, script_path],
      env=env
    )

import requests, pickle

def evaluate_agent(cage_path):

    python_exec = os.path.join(BASE_DIR, "..", cage_path, ".venv", "bin", "python")
    script_path = os.path.join(BASE_DIR, "..", cage_path, "Testing", "evaluate_agent.py")

    env = os.environ.copy()
    env["PYTHONPATH"] = "/home/gabriel/Exploring-CyberGym/Cage4/cage-challenge-4"

    subprocess.Popen(
       [python_exec, script_path],
      env=env
    )

def create_graph(idx):
    
    collected_networks = None
    try:
        with open("graph.pkl", "rb") as f:
           collected_networks = pickle.load(f)
    except FileNotFoundError:
        print("File not found!")
        return None

    fig = collected_networks[idx]
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
    html.H2("Choose Cage"),
    dcc.Dropdown(
        cages,
        'cage-challenge-1',
        id='choose-cage'
    ),
    dcc.Button("Train", id="train", n_clicks=0),
    dcc.Button("Evaluate", id="evaluate", n_clicks=0),
    html.P(id='dummy'),
    dcc.Store(id="cage-path")

]), html.Div([
    html.H2("Rede Interativa"),
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
    id="slider-container",
    children=[
        dcc.Slider(
            0,
            5,
            value=0,
            id="network-slider"
            )
    ],
    style={"display": "none"}  # esconde aqui
    ),

]), html.Footer([
    html.H5("This is a scientific initiation project that uses CybORG research gym")
])

@app.callback(
    Output('network-graph', 'figure'),
    Input('network-slider', 'value'),
    prevent_initial_call=True
)
def update_graph(value):
    fig = create_graph(value)
    return fig

@app.callback(
    Output('network-graph', 'style'),
    Output('slider-container', 'style'),
    Input('evaluate', 'n_clicks'),
    State('cage-path', 'data'),
    prevent_initial_call=True
)
def evaluate(n_clicks, data):
    visible_style = {"display": "block"}
    evaluate_agent(data)
    #update_graph(0)
    return visible_style, visible_style

@app.callback(
    Output('cage-path', 'data'),
    Input('choose-cage', 'value')
)
def choose_cage(value):
    return value

@app.callback(
    Output('dummy', 'children'),
    Input('train', 'n_clicks'),
    State('cage-path', 'data'),
    prevent_initial_call=True
)
def train(n_clicks, data):
    return start_training(data)


if __name__ == "__main__":
    app.run(debug=True)
