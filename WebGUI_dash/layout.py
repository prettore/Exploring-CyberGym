from dash import html, dcc

# Agent files variable
AGENT_FILES = ()

# Listing possible environments
CAGES = ['Cage4']

layout = html.Div([

    html.H3('Choose Cage'),

    dcc.Dropdown(
        options = CAGES,
        id='choose-cage',
        style={'margin':'20px 0px'}
    ),

    dcc.Store(id='cage-path', data='None'),

    html.H4('Training Parameters', style={'marginTop': '20px'}),
    html.Div([
        html.Div([
            html.Label('Steps:'),
            dcc.Input(id='train-steps', type='number', value=1, min=1, style={'width': '100px'}),
        ], style={'display': 'flex', 'flexDirection': 'column'}),
        html.Div([
            html.Label('Learning Rate:'),
            dcc.Input(id='train-lr', type='number', value=0.0001, step=0.0001, style={'width': '100px'}),
        ], style={'display': 'flex', 'flexDirection': 'column'}),
        html.Div([
            html.Label('Batch Size:'),
            dcc.Input(id='train-batch', type='number', value=200, min=10, style={'width': '100px'}),
        ], style={'display': 'flex', 'flexDirection': 'column'}),
    ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}),

    dcc.Graph(
        id='live-train-graph',
        style={'display': 'none'},
        figure={
            'data': [],
            'layout': {}
        }
    ),

    html.P(id='train-loading'),

    html.P(id='train-warning'),

    dcc.Button('Train', id='train', n_clicks=0),

    html.H3('Choose Agent'),

    dcc.Dropdown(
        value = '',
        id='choose-agent',
        style={'margin':'20px 0px'}
    ),

    dcc.Store(id='agent-path', data='None'),

    html.Div(id="eval-loading"),

    html.P(id='eval-warning'),

    html.Div([
        html.Label('Evaluation Steps:'),
        dcc.Input(
            id='eval-steps', 
            type='number', 
            value=50, 
            min=1, 
            style={'width': '100px', 'marginLeft': '10px'}
        )
    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),

    dcc.Button('Evaluate', id='eval', n_clicks=0),

    html.P(id='dummy'),

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

    # Debounced slider for smoother interaction
    dcc.Interval(
        id="slider-debounce",
        interval=100,
        n_intervals=0,
        disabled=True,
        max_intervals=1
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
    ),

    dcc.Interval(
        id="sleep",
        interval=1000,
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

    dcc.Graph(
        id='rewards-graph',
        figure={
            'data': [],
            'layout': {}
        },
        style={'height': '30vh',
        'display': 'none'}
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
        #dcc.Button('^', id='show_actions')
    ),

    html.P(id='actions', style={'display': 'block'}),

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
    style={'display': 'none'}  # esconde aqui

    ),

]), html.Footer([

    html.H5('This is a scientific initiation project that uses CybORG research gym')

])
