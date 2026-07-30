from dash.dependencies import Input, Output, State
from dash import html, dcc
import os
import dash
import plotly.graph_objs as go
from app import app
import subprocess

from utils import (
    list_trained_agents,
    delete_files_on_startup,
    start_training,
    evaluate_agent,
    create_graph,
    get_actions,
    get_rewards,
    create_reward_figure,
    clear_cache,
    get_live_train_data,
)


def _build_live_train_figure():
    """Build a reward-over-steps figure from the live training JSON file."""
    data = get_live_train_data()
    if not data:
        fig = go.Figure()
        fig.update_layout(
            title=dict(
                text='Live Training — Mean Reward per Step',
                font=dict(size=16, color='#FFFFFF')
            ),
            xaxis_title='Training Step',
            yaxis_title='Reward',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#64748B', family='Outfit'),
            xaxis=dict(showgrid=True, gridcolor='#1E293B', zeroline=False),
            yaxis=dict(showgrid=True, gridcolor='#1E293B', zeroline=False),
            margin=dict(l=40, r=40, t=50, b=45)
        )
        return fig

    x = [d['step'] + 1 for d in data]
    y_mean = [d.get('reward_mean', d.get('reward', 0.0)) for d in data]
    y_min = [d.get('reward_min', d.get('reward', 0.0)) for d in data]
    y_max = [d.get('reward_max', d.get('reward', 0.0)) for d in data]

    fig = go.Figure()

    # Min line (invisible, serves as lower boundary for filled area)
    fig.add_trace(go.Scatter(
        x=x,
        y=y_min,
        mode='lines',
        line=dict(width=0),
        hoverinfo='skip',
        showlegend=False,
    ))

    # Max line (filled to next line - which is the min line)
    fig.add_trace(go.Scatter(
        x=x,
        y=y_max,
        mode='lines',
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(0, 240, 255, 0.12)',
        name='Min-Max Range',
        hoverinfo='skip',
    ))

    # Mean Reward line
    fig.add_trace(go.Scatter(
        x=x,
        y=y_mean,
        mode='lines+markers',
        name='Mean Reward',
        line=dict(color='#00F0FF', width=3),
        marker=dict(size=6, color='#0072FF', line=dict(color='#00F0FF', width=1)),
    ))

    fig.update_layout(
        title=dict(
            text='Live Training — Mean Reward & Variance',
            font=dict(size=16, color='#FFFFFF')
        ),
        xaxis_title='Training Step',
        yaxis_title='Episode Reward',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8', family='Outfit'),
        xaxis=dict(
            showgrid=True,
            gridcolor='#1E293B',
            zeroline=False,
            dtick=1
        ),
        yaxis=dict(showgrid=True, gridcolor='#1E293B', zeroline=False),
        margin=dict(l=40, r=40, t=50, b=45),
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#E2E8F0')
        )
    )
    return fig


# Subprocess handles for background training and evaluation
train_process = None
eval_process = None

@app.callback(
    Output('cage-path', 'data'),
    Input('choose-cage', 'value'),
)
def choose_cage(cage):
    return cage

@app.callback(
    Output('agent-path', 'data'),
    Input('choose-agent', 'value'),
    prevent_initial_call=True
)
def choose_agent(agent):
    return agent


@app.callback(
    Output('slider-debounce', 'disabled'),
    Output('slider-debounce', 'n_intervals'),
    Input('network-slider', 'value'),
    prevent_initial_call=True
)
def trigger_slider_debounce(value):
    return False, 1

@app.callback(
    Output('network-graph', 'figure', allow_duplicate=True),
    Output('rewards-graph', 'figure', allow_duplicate=True),
    Output('actions', 'children'),
    Input('slider-debounce', 'n_intervals'),
    State('network-slider', 'value'),
    prevent_initial_call=True
)
def update_graph_debounced(n_intervals, value):
    fig = create_graph(value)
    all_actions = get_actions()
    actions = all_actions[value] if all_actions and value < len(all_actions) else {}
    reward_fig = create_reward_figure(value)
    
    return fig, reward_fig, html.Div([
        html.Div(f"{agent}: {action}", style={'margin': '4px 0', 'padding': '8px', 'backgroundColor': '#1E293B', 'borderRadius': '6px', 'color': '#E2E8F0'}) 
        for agent, action in actions.items()
    ]) 


# Callback for checking if the training is complete
@app.callback(
    Output('train-loading', 'children'),
    Output('train-poller', 'disabled', allow_duplicate=True),
    Output('choose-agent', 'options'),
    Output('live-train-graph', 'figure', allow_duplicate=True),
    Output('train-running', 'data', allow_duplicate=True),
    Output('global-status-text', 'children', allow_duplicate=True),
    Output('global-status-badge', 'className', allow_duplicate=True),
    Output('stat-train-step', 'children', allow_duplicate=True),
    Output('stat-mean-reward', 'children', allow_duplicate=True),
    Output('stat-max-reward', 'children', allow_duplicate=True),
    Input('train-poller', 'n_intervals'),
    State('train-running', 'data'),
    State('cage-path', 'data'),
    prevent_initial_call=True
)
def check_train(n, running, cage):
    global train_process

    if not running or train_process is None:
        return '', True, dash.no_update, dash.no_update, False, "Idle", "status-badge", "N/A", "N/A", "N/A"

    live_fig = _build_live_train_figure()

    data = get_live_train_data()
    if data:
        current_step = str(data[-1]['step'] + 1)
        mean_reward = f"{data[-1].get('reward_mean', data[-1].get('reward', 0.0)):.2f}"
        max_reward = f"{max(d.get('reward_max', d.get('reward', 0.0)) for d in data):.2f}"
    else:
        current_step = "0"
        mean_reward = "0.00"
        max_reward = "0.00"

    # Still training
    if train_process.poll() is None:
        agent_files = list_trained_agents(cage)
        return (
            'Training...', 
            False, 
            agent_files, 
            live_fig, 
            True, 
            "Training Agent...", 
            "status-badge running",
            current_step,
            mean_reward,
            max_reward
        )

    # Completed training
    agent_files = list_trained_agents(cage)
    if train_process.returncode != 0:
        return (
            f'Training failed (exit code {train_process.returncode})', 
            True, 
            agent_files, 
            live_fig, 
            False, 
            "Training Failed", 
            "status-badge failed",
            current_step,
            mean_reward,
            max_reward
        )
        
    return (
        'Finished!', 
        True, 
        agent_files, 
        live_fig, 
        False, 
        "Finished!", 
        "status-badge finished",
        current_step,
        mean_reward,
        max_reward
    )


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
    Output('global-status-text', 'children', allow_duplicate=True),
    Output('global-status-badge', 'className', allow_duplicate=True),
    Output('stat-train-step', 'children', allow_duplicate=True),
    Output('stat-mean-reward', 'children', allow_duplicate=True),
    Output('stat-max-reward', 'children', allow_duplicate=True),
    Input('train', 'n_clicks'),
    State('cage-path', 'data'),
    State('train-steps', 'value'),
    State('train-lr', 'value'),
    State('train-batch', 'value'),
    prevent_initial_call=True
)
def train(n_clicks, data, steps, lr, batch_size):
    if data == None:
        return 'Choose a Cage first!', False, True, False, "Idle", "status-badge", dash.no_update, dash.no_update, dash.no_update

    global train_process
    # If it is already training, do nothing
    if train_process and train_process.poll() is None:
        return 'Already training!', False, False, True, "Training Agent...", "status-badge running", dash.no_update, dash.no_update, dash.no_update
        
    # Start fresh training metrics
    webgui_dir = os.path.dirname(os.path.abspath(__file__))
    live_train_path = os.path.join(webgui_dir, 'live_train.json')
    try:
        if os.path.exists(live_train_path):
            os.remove(live_train_path)
    except OSError:
        pass

    train_process = start_training(data, steps, lr, batch_size)
    return '', True, False, True, "Training Agent...", "status-badge running", "0", "0.00", "0.00"


# Callback for checking if the evaluation is complete
@app.callback(
    Output('eval-loading', 'children'),
    Output('eval-poller', 'disabled', allow_duplicate=True),
    Output('eval-running', 'data', allow_duplicate=True),
    Output('global-status-text', 'children', allow_duplicate=True),
    Output('global-status-badge', 'className', allow_duplicate=True),
    Input('eval-poller', 'n_intervals'),
    State('eval-running', 'data'),
    prevent_initial_call=True
)
def check_eval(n, running):
    global eval_process

    if not running or eval_process is None:
        return '', True, False, "Idle", "status-badge"

    if eval_process.poll() is None:
        return 'Evaluating...', False, True, "Evaluating Agent...", "status-badge running"

    if eval_process.returncode != 0:
        return f'Evaluation failed (exit code {eval_process.returncode})', True, False, "Evaluation Failed", "status-badge failed"
    return 'Finished!', True, False, "Finished!", "status-badge finished"


@app.callback(
    Output('eval-warning', 'children', allow_duplicate=True),
    Output('eval-warning-clear', 'disabled', allow_duplicate=True),
    Output('eval-poller', 'disabled', allow_duplicate=True),
    Output('eval-running', 'data'),
    Output('network-graph', 'style', allow_duplicate=True),
    Output('rewards-graph', 'style', allow_duplicate=True),
    Output('slider-container', 'style', allow_duplicate=True),
    Output('network-slider', 'max'),
    Output('network-slider', 'marks'),
    Output('play-container', 'style', allow_duplicate=True),
    Output('pause-container', 'style', allow_duplicate=True),
    Output('global-status-text', 'children', allow_duplicate=True),
    Output('global-status-badge', 'className', allow_duplicate=True),
    Input('eval', 'n_clicks'),
    State('cage-path', 'data'),
    State('agent-path', 'data'),
    State('eval-steps', 'value'),
    prevent_initial_call=True
)
def eval(n_clicks, cage, agent, steps):
    if agent == None:
        return (
            'Choose an agent first!', False, False, False, 
            {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, 
            dash.no_update, dash.no_update, {'display': 'none'}, {'display': 'none'}, 
            "Idle", "status-badge"
        )

    global eval_process
    if eval_process and eval_process.poll() is None:
        return (
            'Already evaluating!', False, False, True, 
            {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, 
            dash.no_update, dash.no_update, {'display': 'none'}, {'display': 'none'}, 
            "Evaluating Agent...", "status-badge running"
        )

    clear_cache()

    eval_process = evaluate_agent(cage, agent, steps)

    step_marks = {i: str(i) for i in range(0, steps + 1, max(1, steps // 10))}

    return (
        '', True, False, True, 
        {'display': 'block', 'height': '60vh'}, 
        {'display': 'block', 'height': '30vh'}, 
        {'display': 'block'}, 
        steps, 
        step_marks, 
        {'display': 'inline-block'}, 
        {'display': 'inline-block'}, 
        "Evaluating Agent...", 
        "status-badge running"
    )


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


# --- Play / Pause controls ---------------------------------------------------

@app.callback(
    Output('sleep', 'disabled'),
    Input('start', 'n_clicks'),
    Input('pause', 'n_clicks'),
    prevent_initial_call=True
)
def control_playback(start_clicks, pause_clicks):
    trigger_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    return trigger_id == 'pause'  # False (enabled) when Play, True (disabled) when Pause


@app.callback(
    Output('network-slider', 'value', allow_duplicate=True),
    Output('sleep', 'disabled', allow_duplicate=True),
    Input('sleep', 'n_intervals'),
    State('network-slider', 'value'),
    State('network-slider', 'max'),
    prevent_initial_call=True
)
def advance_slider(n, current_val, max_val):
    """Advance the slider by one step; stop automatically at the end."""
    next_val = (current_val or 0) + 1
    if next_val >= (max_val or 0):
        return max_val, True  # reached end — disable interval
    return next_val, False