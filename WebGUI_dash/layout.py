from dash import html, dcc

# Agent files variable
AGENT_FILES = ()

# Listing possible environments
CAGES = ['Cage4']

layout = html.Div(
    className="dashboard-container",
    children=[
        # Left Sidebar (Controls)
        html.Div(
            className="sidebar",
            children=[
                html.Div(
                    className="sidebar-brand",
                    children=[
                        html.I(className="fa-solid fa-shield-halved", style={"marginRight": "8px"}),
                        html.Span("CyberGym Dash")
                    ]
                ),
                
                # Cage Selection
                html.Div(
                    className="sidebar-section",
                    children=[
                        html.Div("Environment Configuration", className="sidebar-section-title"),
                        html.Div(
                            className="config-card",
                            children=[
                                html.Div(
                                    className="form-group",
                                    children=[
                                        html.Label("Choose Cage:"),
                                        dcc.Dropdown(
                                            options=CAGES,
                                            id='choose-cage',
                                            placeholder="Select a Cage..."
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),

                # Training Configuration
                html.Div(
                    className="sidebar-section",
                    children=[
                        html.Div("Agent Training", className="sidebar-section-title"),
                        html.Div(
                            className="config-card",
                            children=[
                                html.Div(
                                    className="form-row",
                                    children=[
                                        html.Div(
                                            className="form-group",
                                            children=[
                                                html.Label("Steps:"),
                                                dcc.Input(id='train-steps', type='number', value=5, min=1)
                                            ]
                                        ),
                                        html.Div(
                                            className="form-group",
                                            children=[
                                                html.Label("Batch:"),
                                                dcc.Input(id='train-batch', type='number', value=200, min=10)
                                            ]
                                        )
                                    ]
                                ),
                                html.Div(
                                    className="form-group",
                                    children=[
                                        html.Label("Learning Rate:"),
                                        dcc.Input(id='train-lr', type='number', value=0.0001, step=0.0001)
                                    ]
                                ),
                                html.Button(
                                    children=[html.I(className="fa-solid fa-graduation-cap", style={"marginRight": "8px"}), "Train Agent"],
                                    id='train',
                                    className="btn btn-primary",
                                    n_clicks=0
                                ),
                                html.Div(id='train-warning', className="warning-message")
                            ]
                        )
                    ]
                ),

                # Evaluation Configuration
                html.Div(
                    className="sidebar-section",
                    children=[
                        html.Div("Agent Evaluation", className="sidebar-section-title"),
                        html.Div(
                            className="config-card",
                            children=[
                                html.Div(
                                    className="form-group",
                                    children=[
                                        html.Label("Choose Agent:"),
                                        dcc.Dropdown(
                                            id='choose-agent',
                                            placeholder="Select an Agent..."
                                        )
                                    ]
                                ),
                                html.Div(
                                    className="form-group",
                                    children=[
                                        html.Label("Evaluation Steps:"),
                                        dcc.Input(id='eval-steps', type='number', value=50, min=1)
                                    ]
                                ),
                                html.Button(
                                    children=[html.I(className="fa-solid fa-chart-line", style={"marginRight": "8px"}), "Evaluate Agent"],
                                    id='eval',
                                    className="btn btn-secondary",
                                    n_clicks=0
                                ),
                                html.Div(id='eval-warning', className="warning-message")
                            ]
                        )
                    ]
                )
            ]
        ),

        # Right Main Panel
        html.Div(
            className="main-content",
            children=[
                # Top Header with status
                html.Div(
                    className="main-header",
                    children=[
                        html.Div(
                            className="header-title-container",
                            children=[
                                html.H1("CyberGym Research Dashboard"),
                                html.P("Interactive training & evaluation interface using CybORG gym")
                            ]
                        ),
                        html.Div(
                            id="global-status-badge",
                            className="status-badge",
                            children=[
                                html.Div(className="pulse-dot"),
                                html.Span("Idle", id="global-status-text")
                            ]
                        )
                    ]
                ),

                # Stat Cards (Live training metrics)
                html.Div(
                    className="stat-cards-grid",
                    children=[
                        html.Div(
                            className="stat-card",
                            children=[
                                html.Div("Current Training Step", className="stat-card-title"),
                                html.Div("N/A", id="stat-train-step", className="stat-card-value")
                            ]
                        ),
                        html.Div(
                            className="stat-card",
                            children=[
                                html.Div("Mean Reward", className="stat-card-title"),
                                html.Div("N/A", id="stat-mean-reward", className="stat-card-value")
                            ]
                        ),
                        html.Div(
                            className="stat-card",
                            children=[
                                html.Div("Max Reward Achieved", className="stat-card-title"),
                                html.Div("N/A", id="stat-max-reward", className="stat-card-value")
                            ]
                        )
                    ]
                ),

                # Main visualization tabs
                html.Div(
                    className="tabs-container",
                    children=[
                        dcc.Tabs(
                            id="visualizer-tabs",
                            value="tab-training",
                            className="custom-tabs",
                            children=[
                                # Tab 1: Live Training Visualization
                                dcc.Tab(
                                    label="Live Training Progress",
                                    value="tab-training",
                                    className="custom-tab",
                                    selected_className="custom-tab active",
                                    children=[
                                        html.Div([
                                            html.Div(id='train-loading', style={'marginTop': '10px', 'fontWeight': '600', 'color': '#00F0FF'}),
                                            html.Div(
                                                className="graph-container",
                                                style={"marginTop": "15px"},
                                                children=[
                                                    dcc.Graph(
                                                        id='live-train-graph',
                                                        style={'height': '55vh'},
                                                        figure={
                                                            'data': [],
                                                            'layout': {'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)'}
                                                        }
                                                    )
                                                ]
                                            )
                                        ])
                                    ]
                                ),

                                # Tab 2: Interactive Network & Evaluation
                                dcc.Tab(
                                    label="Evaluation Network & Rewards",
                                    value="tab-evaluation",
                                    className="custom-tab",
                                    selected_className="custom-tab active",
                                    children=[
                                        html.Div([
                                            html.Div(id="eval-loading", style={'marginTop': '10px', 'fontWeight': '600', 'color': '#10B981'}),
                                            
                                            html.H3('Rede Interativa', style={'margin': '20px 0 10px 0', 'fontSize': '16px', 'fontWeight': '600'}),
                                            html.Div(
                                                className="graph-container",
                                                children=[
                                                    dcc.Graph(
                                                        id='network-graph',
                                                        figure={'data': [], 'layout': {}},
                                                        style={'display': 'none', 'height': '60vh'}
                                                    )
                                                ]
                                            ),

                                            html.H3('Evaluation Cumulative Rewards', style={'margin': '20px 0 10px 0', 'fontSize': '16px', 'fontWeight': '600'}),
                                            html.Div(
                                                className="graph-container",
                                                children=[
                                                    dcc.Graph(
                                                        id='rewards-graph',
                                                        figure={'data': [], 'layout': {}},
                                                        style={'display': 'none', 'height': '30vh'}
                                                    )
                                                ]
                                            ),

                                            html.Div(
                                                className="playback-controls",
                                                children=[
                                                    html.Div(
                                                        id='play-container',
                                                        style={'marginRight': '10px', 'display': 'none'},
                                                        children=[dcc.Button('▶ Play', id='start', className="btn btn-primary")]
                                                    ),
                                                    html.Div(
                                                        id='pause-container',
                                                        style={'display': 'none'},
                                                        children=[dcc.Button('⏸ Pause', id='pause', className="btn btn-secondary")]
                                                    )
                                                ]
                                            ),

                                            html.Div(
                                                className="slider-container-box",
                                                id='slider-container',
                                                style={'display': 'none'},
                                                children=[
                                                    dcc.Slider(
                                                        0,
                                                        50,
                                                        value=0,
                                                        id='network-slider'
                                                    )
                                                ]
                                            ),

                                            html.Div(
                                                className="actions-log",
                                                id='actions'
                                            )
                                        ])
                                    ]
                                )
                            ]
                        )
                    ]
                ),

                # Footer
                html.Footer(
                    className="footer",
                    children=[
                        html.H5("Scientific initiation project utilizing the CybORG cyber security gym")
                    ]
                )
            ]
        ),

        # Hidden stores & utilities
        dcc.Store(id='cage-path', data='None'),
        dcc.Store(id='agent-path', data='None'),
        dcc.Store(id="train-running", data=False),
        dcc.Store(id="eval-running", data=False),
        
        dcc.Interval(id="train-poller", interval=1000, disabled=True),
        dcc.Interval(id="eval-poller", interval=1000, disabled=True),
        dcc.Interval(id="slider-debounce", interval=100, n_intervals=0, disabled=True, max_intervals=1),
        dcc.Interval(id="train-warning-clear", interval=2000, n_intervals=0, disabled=True),
        dcc.Interval(id="eval-warning-clear", interval=2000, n_intervals=0, disabled=True),
        dcc.Interval(id="sleep", interval=500, n_intervals=0, disabled=True)
    ]
)
