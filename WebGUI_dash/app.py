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

    subprocess.Popen([
        python_exec,
        script_path
    ])

import requests, json

def evaluate_agent(cage_path):

    python_exec = os.path.join(BASE_DIR, "..", cage_path, ".venv", ".bin", "python")
    script_exec = os.path.join(BASE_DIR, "..", cage_path, "Testing", "evaluate_agent.py")

    subprocess.Popen([
        python_exec,
        script_path
    ])

    data = None
    try:
        with open("../Cage4/Testing/graph.json") as f: # Aqui deve ser alterado!
            data = json.load(f)
    except FileNotFoundError:
        print("File not found!")
        return None

    G = nx.node_link_graph(data[0]['network_map'])

    # generate plot
    pos = nx.spring_layout(G, seed=42)

    # Edge traces
    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1),
        hoverinfo='none',
        mode='lines'
    )

    # Node traces
    node_x = []
    node_y = []
    node_text = []
    node_color = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"{node}<br>Valor: {G.nodes[node]['value']}")
        node_color.append(G.degree[node])

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=True,
            colorscale='Viridis',
            color=node_color,
            size=15,
            colorbar=dict(
                title="Grau"
            ),
            line_width=2
        )
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=0, l=0, r=0, t=0),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )

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
    dcc.Button("Train!", id="train", n_clicks=0),
    dcc.Button("Create graph", id="refresh-graph", n_clicks=0),
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
        style={'height': '80vh'},
        style={'display': 'none'}
    ),
    dcc.Button('>', id='start'),  # Ao apertar o botão, o Slider será movimentado automaticamente!
    dcc.Button('||', id='pause'), # pausa!
    dcc.Slider( # cada numero do slider vai desenhar um 
        0,
        50,
        value=0,
        id="network-slider",
        style={'display': 'none'}
    )
]), html.Footer([
    html.H5("This is a scientific initiation project that uses CybORG research gym")
])

@app.callback(
    Output('network-graph', 'figure'),
    Output('network-graph', 'style'),
    Output('network-slider', 'style'),
    Input('network-slider', 'value'),
    State('cage-path', 'data'),
    prevent_initial_call=True
)
def update_graph(n_clicks, data):
    fig = import_graph(data)
    return import_graph(data)

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
