from dash import html, dcc

# Agent files variable
AGENT_FILES = ()

# Listing possible environments
CAGES = ['Cage4']

layout = html.Div([

    html.H3('Choose Cage'),

    dcc.Dropdown(
        options = CAGES,
        value = 'Cage4',
        id='choose-cage',
        style={'margin':'20px 0px'}
    ),

    dcc.Store(id='cage-path', data='None'),

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
