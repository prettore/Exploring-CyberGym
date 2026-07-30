import networkx as nx
from networkx import connected_components
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import time
import numpy as np
from copy import deepcopy

from CybORG import CybORG
from CybORG.Simulator.Scenarios.EnterpriseScenarioGenerator import SUBNET
from CybORG.Simulator.Scenarios import EnterpriseScenarioGenerator
from CybORG.Agents.SimpleAgents.ConstantAgent import SleepAgent
from CybORG.Agents.SimpleAgents.FiniteStateRedAgent import FiniteStateRedAgent
from CybORG.Agents import SleepAgent, EnterpriseGreenAgent

import plotly.graph_objects as go

from networkx.readwrite import json_graph

class VisualiseRedExpansionMod():
    """
        This is a slightly modified version of the CybORG class VisualizeRedExpansion.
        It is intended to be usable on wrapped cyborg class. (e.g. EnterpriseMAE)
    """

    """Visualisation wrapper that displays the user and root shells acquired by red agents over time, in a series of network graph plots. 
    
    Attributes
    ----------
    actions:

    obs:

    fig : matplotlib.pyplot.figure.Figure (plotly.go.figure)
        graph figure
    ax : matplotlib.pyplot.axes.Axes ()
        graph axes
    slider : matplotlib.widgets.Slider
        slider to control graph in GUI
    collected_networks : networkx.Graph
        graph of the network
    play_view_flag : bool
        flag for if the graph display is iterating through steps
    env : SimulationController
        CybORG environment used
    total_steps : int
        total number of steps to iterate over
    node_label_mapping : Dict[str, str]
        dictionary mapping host names to the abbreviated labels shown of the graph
    host_nodes : Dict[str, str]
        grouping of host types to hosts
    host_interfaces : list
        list of interfaces as edges between two hosts
    pos : Dict[str, float]
        position of nodes on graph
    """
    def __init__(self, cyborg, steps):
        self.fig = None
        self.ax = None
        self.slider = None
        self.collected_networks = []
        self.play_view_flag = False
        
        self.env = cyborg.environment_controller
        self.total_steps = steps

        # Fixed graph nodelists (of host) 
        env_netmap = self.env.state.link_diagram.copy()
        self.node_label_mapping = self._get_node_label_mapping(env_netmap)
        self.host_nodes = self._get_host_nodes(env_netmap)
        self.host_interfaces = list(env_netmap.edges()).copy()
 
        # Create initial network nodelists
        initial_network_info = self._set_initial_agents_and_sessions()

        # Add the new edges and nodes to the graph
        env_netmap.add_nodes_from(initial_network_info['active_agents']['blue'])
        env_netmap.add_edges_from(initial_network_info['host_sessions'])

        self.pos = self._set_network_host_and_agents_positions(env_netmap)
        env_netmap.add_nodes_from(initial_network_info['active_agents']['red'])

        initial_network_info['network_map'] = env_netmap
        self.collected_networks.append(initial_network_info)

        # New attributes for keeping the actions and cyborg observations
        self.all_actions = []
        self.all_obs = {}

    def run(self):
        """Automating the running of the visualisation, with visualising each step then outputting the graph."""
        for step in range(self.total_steps):
            self.env.step()
            self.visualise_step()
        self.show_graph()

    def modified_run(self, cyborg):
        self.env = cyborg.environment_controller
        self.visualise_step()

        # Do this on eval.py # self.show_graph()
    
    def visualise_step(self):
        """Collecting all the information at each step and adding it to a dictionary, to be used later for the visualisation. """
        
        host_nodes_compromised, red_agents = self._get_compromised_nodes()
        all_session_agents, all_host_sessions, agent_label_mapping, red_root_nodes = self._get_compromised_edges()
        
        actions = {}

        for agent in self.env.team['Red'] + self.env.team['Blue']:
            try:
                actions[agent] = self.env.get_last_action(agent)[0].__class__.__name__
            except Exception as err:
                # print(f"[ERROR] An error occurred in action mapping: {err}")
                actions[agent] = None

        self.all_actions.append(actions)

        known_red_agents = self.collected_networks[-1]['active_agents']['red']

        if len(all_session_agents['red'])>len(known_red_agents):
            new_network = self.collected_networks[-1]['network_map'].copy()
            for new_red in all_session_agents['red']:
                if new_red not in known_red_agents:
                    new_network.add_node(new_red)

            new_network_info = {
                'network_map' : new_network,
                'active_agents' : all_session_agents,
                'agent_label_mapping' : agent_label_mapping,
                'host_sessions' : all_host_sessions,
                'compromised_hosts' : host_nodes_compromised,
                'red_root_nodes' : red_root_nodes
            }
        else:
            new_network_info = {
                'network_map' : self.collected_networks[-1]['network_map'],
                'active_agents' : all_session_agents,
                'agent_label_mapping' : agent_label_mapping,
                'host_sessions' : all_host_sessions,
                'compromised_hosts' : host_nodes_compromised,
                'red_root_nodes' : red_root_nodes
            }

        self.collected_networks.append(new_network_info)

    def _btn_forward(self, ev):
        pos = self.slider.val
        if pos < self.total_steps:
            self.slider.set_val(pos+1)

    def _btn_back(self, ev):
        pos = self.slider.val
        if pos > 0:
            self.slider.set_val(pos-1)
    
    def _btn_play(self, ev):
        self.play_view_flag = True

        while self.play_view_flag:
            pos = self.slider.val
            if pos < self.total_steps:
                self.slider.set_val(pos+1)
            else:
                self.play_view_flag = False
            plt.pause(0.3)

    def _btn_pause(self, ev):
        self.play_view_flag = False

    def get_figures(self, init: bool = False):
        import copy

        collected_networks = copy.copy(self.collected_networks)

        figures = []

        # usa posições fixas calculadas no init
        pos = dict(self.pos)

        for idx, G_dict in enumerate(collected_networks):

            G = G_dict['network_map']

            # garante posição para novos nós
            for n in G.nodes():
                if n not in pos:
                    pos[n] = np.random.rand(2)

            traces = []

            # ======================
            # EDGES
            # ======================
                
            def make_edges(edgelist, dash=None, color='black'):
                edge_x, edge_y = [], []
                for u, v in edgelist:
                    if u not in pos or v not in pos:
                        continue
                    x0, y0 = pos[u]
                    x1, y1 = pos[v]
                    edge_x += [x0, x1, None]
                    edge_y += [y0, y1, None]

                return go.Scatter(
                    x=edge_x,
                    y=edge_y,
                    mode='lines',
                    line=dict(width=1, dash=dash, color=color),
                    hoverinfo='none',
                    showlegend=False  # added
                )

            # fixed edges of the network (black)
            traces.append(make_edges(self.host_interfaces))

            # red agent sessions (dotted red)
            red_sessions = [(host, agent) for host, agent in G_dict['host_sessions'] if 'red' in agent]
            if red_sessions:
                traces.append(make_edges(red_sessions, dash='dot', color='red'))

            # blue agent sessions (dotted blue)
            blue_sessions = [(host, agent) for host, agent in G_dict['host_sessions'] if 'blue' in agent]
            if blue_sessions:
                traces.append(make_edges(blue_sessions, dash='dot', color='blue'))

            # ======================
            # NODES
            # ======================

            def make_nodes(nodelist, color, symbol, size=200, alpha=1, labels=None):
                x, y, text = [], [], []

                for i, n in enumerate(nodelist):
                    if n not in pos:
                        continue
                    xi, yi = pos[n]
                    x.append(xi)
                    y.append(yi)
                    text.append(labels[i] if labels and i < len(labels) else str(n))

                return go.Scatter(
                    x=x,
                    y=y,
                    mode='markers',
                    marker=dict(
                        size=size / 20,
                        color=color,
                        symbol=symbol,
                        opacity=alpha
                    ),
                    text=text,
                    hoverinfo='text',
                    showlegend=False
                )
            # ======================
            # HOST TYPES
            # ======================

            traces.append(make_nodes(
                self.host_nodes['users'], '#C0C0C0', 'circle',
                labels=[f"💻 {n}" for n in self.host_nodes['users']]
            ))
            traces.append(make_nodes(
                self.host_nodes['servers'], '#C0C0C0', 'square',
                labels=[f"🖥️ {n}" for n in self.host_nodes['servers']]
            ))
            traces.append(make_nodes(
                self.host_nodes['other'], '#C0C0C0', 'hexagon',
                labels=[f"🌐 {n}" for n in self.host_nodes['other']]
            ))

            # ======================
            # AGENTS
            # ======================

            traces.append(make_nodes(
                G_dict['active_agents']['red'], '#EE4B2B', 'triangle-up',
                labels=[f"🚨 {n} (red agent)" for n in G_dict['active_agents']['red']]
            ))
            traces.append(make_nodes(
                G_dict['active_agents']['blue'], '#0096FF', 'triangle-up',
                labels=[f"🛡️ {n} (blue agent)" for n in G_dict['active_agents']['blue']]
            ))

            # ======================
            # STATES
            # ======================

            traces.append(make_nodes(
                G_dict['compromised_hosts'], '#FFA500', 'circle', alpha=0.8,
                labels=[f"⚠️ {n} (compromised)" for n in G_dict['compromised_hosts']]
            ))
            traces.append(make_nodes(
                G_dict['red_root_nodes'], '#EE4B2B', 'circle', alpha=0.8,
                labels=[f"🔴 {n} (root access)" for n in G_dict['red_root_nodes']]
            ))

            # ======================
            # ROUTER LABELS
            # ======================

            router_x = []
            router_y = []
            router_text = []

            for router, label in self.node_label_mapping.items():
                if router in pos:
                    router_x.append(pos[router][0])
                    router_y.append(pos[router][1])
                    router_text.append(f"<b>{label}</b>")

            if router_x:
                traces.append(
                    go.Scatter(
                        x=router_x,
                        y=router_y,
                        mode='text',
                        text=router_text,
                        textposition='top center',
                        textfont=dict(size=14, color='black'),
                        hoverinfo='none',
                        showlegend=False
                    )
                )

            # ======================
            # FIGURES
            # ======================

            legend_traces = [

                # Hosts
                go.Scatter(
                    x=[None], y=[None],
                    mode='markers',
                    marker=dict(size=10, color='#C0C0C0', symbol='circle'),
                    name='User Hosts',
                    showlegend=True
                ),
                go.Scatter(
                    x=[None], y=[None],
                    mode='markers',
                    marker=dict(size=10, color='#C0C0C0', symbol='square'),
                    name='Servers',
                    showlegend=True
                ),
                go.Scatter(
                    x=[None], y=[None],
                    mode='markers',
                    marker=dict(size=10, color='#C0C0C0', symbol='hexagon'),
                    name='Other Hosts',
                    showlegend=True
                ),

                # Agents
                go.Scatter(
                    x=[None], y=[None],
                    mode='markers',
                    marker=dict(size=10, color='#EE4B2B', symbol='triangle-up'),
                    name='Red Agent',
                    showlegend=True
                ),
                go.Scatter(
                    x=[None], y=[None],
                    mode='markers',
                    marker=dict(size=10, color='#0096FF', symbol='triangle-up'),
                    name='Blue Agent',
                    showlegend=True
                ),

                # States
                go.Scatter(
                    x=[None], y=[None],
                    mode='markers',
                    marker=dict(size=10, color='#FFA500', symbol='circle'),
                    name='Compromised Host',
                    showlegend=True
                ),
                go.Scatter(
                    x=[None], y=[None],
                    mode='markers',
                    marker=dict(size=10, color='#EE4B2B', symbol='circle'),
                    name='Root Access',
                    showlegend=True
                ),
            ]

            fig = go.Figure(data=traces + legend_traces)

            fig.update_layout(
                showlegend=True,
                legend=dict(
                    x=1.02,   # right side
                    y=1,
                    xanchor='left',
                    yanchor='top'
                ),
                xaxis=dict(showgrid=False, zeroline=False, visible=False),
                yaxis=dict(showgrid=False, zeroline=False, visible=False)
            )

            figures.append(fig)
            # print(f"[DEBUG] Figure {idx} added")

        return figures

    # get the compromised nodes for colour coding
    def _get_compromised_nodes(self):
        host_nodes_compromised=[]
        agents_active=[]
        for red_agent_name in self.env.team['Red']:
            for sess in self.env.state.sessions[red_agent_name].values():
                host_nodes_compromised.append(sess.hostname)
                agents_active.append(red_agent_name)
        return list(set(host_nodes_compromised)), list(set(agents_active))

    def _get_compromised_edges(self):
        last_collected_network = self.collected_networks[-1]

        all_session_agents = deepcopy(last_collected_network['active_agents'])
        all_host_sessions = deepcopy(last_collected_network['host_sessions'])
        agent_label_mapping = deepcopy(last_collected_network['agent_label_mapping'])

        agent_root_nodes = self._get_agent_root_nodes()
        red_root_nodes = []

        # For each host in the state, add their agent sessions to the new edges list and the agents to the new nodes list (grouped by agent type)
        for hostname, host in self.env.state.hosts.items():
            for agent, sids in host.sessions.items():
                if not sids == []:
                    if "red" in agent:
                        if agent not in all_session_agents['red']: 
                            all_host_sessions.append((hostname, agent))
                            all_session_agents["red"].append(agent)
                            agent_label_mapping[agent] = "R" + agent.split("_")[-1]
                        for sid in sids:
                            if sid in agent_root_nodes[agent]:
                                red_root_nodes.append(hostname)
                            # agent_label_mapping[hostname] = str(sid)
        #all_session_agents["red"] = list(set(all_session_agents["red"]))
        return all_session_agents, all_host_sessions, agent_label_mapping, red_root_nodes

    def _get_agent_root_nodes(self):
        agent_root_nodes = {}

        for agent, sessions in self.env.state.sessions.items():
            if 'red' in agent:
                agent_root_nodes[agent] = []
                for i, sess in sessions.items():
                    if sess.username == "root":
                        agent_root_nodes[agent].append(i)
        
        return agent_root_nodes

    def _get_node_label_mapping(self, env_netmap):
        # Node label mapping
        node_label_mapping = {}
        for node in env_netmap._node.keys():
            if not "user_host" in node and not "server_host" in node:
                new_node_label = ""
                
                # Zone name
                if "restricted_zone" in node:
                    new_node_label = "RZ"
                elif "operational_zone" in node:
                    new_node_label = "OZ"
                elif "contractor_network" in node:
                    new_node_label = "CN"
                elif "public_access_zone" in node:
                    new_node_label = "PAZ"
                elif "admin_network" in node:
                    new_node_label = "AN"
                elif "office_network" in node:
                    new_node_label = "ON"
                else:
                    new_node_label = "Internet Root"
                    node_label_mapping[node] = new_node_label
                    continue

                # Partition
                if "_a_" in node:
                    new_node_label = new_node_label + "A"
                elif "_b_" in node:
                    new_node_label = new_node_label + "B"

                node_label_mapping[node] = new_node_label

        return node_label_mapping

    def _get_host_nodes(self, env_netmap):
        host_nodes = {}

        all_host_nodes = list(env_netmap.nodes()).copy()
        host_nodes['servers'] = [host for host in all_host_nodes if 'server' in host]
        host_nodes['users'] = [host for host in all_host_nodes if 'user' in host]
        host_nodes['other'] = [host for host in all_host_nodes if 'user' not in host and 'server' not in host]

        return host_nodes

    def _set_initial_agents_and_sessions(self):
        all_session_agents = {"blue": [], "red": []}
        agent_label_mapping = {}
        all_host_sessions = []
        compromised_hosts = []

        agent_root_nodes = self._get_agent_root_nodes()
        red_root_nodes = []

        # For each host in the state, add their agent sessions to the new edges list and the agents to the new nodes list (grouped by agent type)
        for hostname, host in self.env.state.hosts.items():
            for agent, sids in host.sessions.items():
                if not sids == []:
                    if "blue" in agent:
                        all_session_agents["blue"].append(agent)
                        agent_label_mapping[agent] = "B" + agent.split("_")[-1]
                        all_host_sessions.append((hostname, agent))
                    elif "red" in agent:
                        all_session_agents["red"].append(agent)
                        agent_label_mapping[agent] = "R" + agent.split("_")[-1]
                        all_host_sessions.append((hostname, agent))
                        compromised_hosts.append(hostname)

                        for sid in sids:
                            if sid in agent_root_nodes[agent]:
                                red_root_nodes.append(hostname)

        # Duplicates are removed from lists
        all_session_agents["blue"] = list(set(all_session_agents["blue"]))
        all_session_agents["red"] = list(set(all_session_agents["red"]))

        info = {
            'active_agents' : all_session_agents,
            'agent_label_mapping' : agent_label_mapping,
            'host_sessions' : all_host_sessions,
            'compromised_hosts' : compromised_hosts,
            'red_root_nodes' : red_root_nodes
        }
        return info

    def _set_network_host_and_agents_positions(self, env_netmap):
        all_red_agents = ['red_agent_0', 'red_agent_1', 'red_agent_2', 'red_agent_3', 'red_agent_4', 'red_agent_5', ]

        red_agent_allowed_subnets = [
            [SUBNET.CONTRACTOR_NETWORK.value],
            [SUBNET.RESTRICTED_ZONE_A.value],
            [SUBNET.OPERATIONAL_ZONE_A.value],
            [SUBNET.RESTRICTED_ZONE_B.value],
            [SUBNET.OPERATIONAL_ZONE_B.value],
            [SUBNET.PUBLIC_ACCESS_ZONE.value, SUBNET.ADMIN_NETWORK.value, SUBNET.OFFICE_NETWORK.value]
        ]

        positions = nx.spring_layout(env_netmap, seed=2, iterations=300)

        # get the position of hosts in each subnet - used for new red agent positions
        subnet_host_positions = {}
        for subnet in self.env.state.subnets.values():
            subnet_name = subnet.name
            subnet_host_positions[subnet_name] = []
            for host_name in self.env.state.hosts.keys():
                if subnet_name in host_name:
                    subnet_host_positions[subnet_name].append(list(positions[host_name]))
                    
        for r in range(6):
            red_agent_name = 'red_agent_' + str(r)

            if len(red_agent_allowed_subnets[r]) == 1:
                positions[red_agent_name] = np.array(subnet_host_positions[red_agent_allowed_subnets[r][0]]).mean(axis=0)*1.15

            else:
                combined_subnet_hosts = []
                for s in red_agent_allowed_subnets[r]:
                    combined_subnet_hosts.extend(subnet_host_positions[s])
                positions[red_agent_name] = np.array(combined_subnet_hosts).mean(axis=0)*1.15

        return positions