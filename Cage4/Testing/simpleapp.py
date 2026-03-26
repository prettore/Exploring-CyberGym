import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import networkx as nx
import plotly.graph_objs as go
import random
import pandas as pd

import subprocess

import requests, pickle

# Retrieve graph from 'collected_figures'
def create_graph(idx):
    
    collected_figures = None
    try:
        with open('graph.pkl', 'rb') as f:
           collected_figures = pickle.load(f)
    except FileNotFoundError:
        print('File not found!')
        return None

    fig = collected_figures[idx]
    #print(collected_figures[1])
    return fig

# =========================
# App Dash
# =========================
app = dash.Dash(__name__)

app.layout = html.Div([

    html.H2('Rede Interativa'),

    dcc.Graph(
        id='network-graph',
        figure={
            'data': [],
            'layout': {}
        },
        style={'height': '80vh'}
        ),

    html.Div(
        dcc.Button('>', id='start'),  # TODO - Ao apertar o botão, o Slider será movimentado automaticamente!
        style={'display':'none'}
    ),

    html.Div(
        dcc.Button('||', id='pause'), # TODO - pausa!
        style={'display':'none'}
    ),

    html.Div(

    id='slider-container',
    children=[
        dcc.Slider(
            0,
            50,
            value=0,
            id='network-slider'
            )
    ],
    #style={'display': 'none'}  # esconde aqui

    ),

])

@app.callback(
    Output('network-graph', 'figure', allow_duplicate=True),
    Input('network-slider', 'value'),
    prevent_initial_call=True
)
def update_graph(value):
    fig = create_graph(value)
    return fig

if __name__ == '__main__':
    app.run(debug=True)
