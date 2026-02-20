'''

yaml file parser for network visualization.
obs: written as 'router' read as 'switch'

'''
import yaml
import random
from pprint import pprint
import matplotlib.pyplot as plt
import networkx as nx
from CybORG import CybORG
from CybORG.Simulator.Scenarios import EnterpriseScenarioGenerator
import os

sg = EnterpriseScenarioGenerator()

env = CybORG(sg)

state = env.environment_controller.state

G = state.link_diagram

nx.draw(G, with_labels=True, node_color='orange')
plt.savefig("./app/scripts/scenario2.png")

'''
G = nx.Graph()

def add_router(Graph, Router):
    G.add_node("router {}".format(Router))

data = {}

while not (os.path.exists(path)):
    print(path)
    file = input("Error. Try again: ")
    path = cwd + "/../Scenarios/" + file

with open(path, "r") as file:
    data = yaml.safe_load(file)

subnets = data['Subnets'] #dict
hosts = data['Hosts'] #dict

#Look for hosts on the subnet
for subnet, value in subnets.items():

    s_hosts = value['Hosts'] #lista

    #add subnet router
    G.add_node(subnet, subnet=subnet)
    
    for s_host in s_hosts:

        G.add_node(s_host, subnet=subnet)
        G.add_edge(subnet, s_host)

        if "info" not in hosts[s_host].keys():
            continue

        info = hosts[s_host]["info"]

        for visible, interface in info.items():
            # descobre qual é a subrede do potencial vizinho
            for s, v in subnets.items():
                if visible in v['Hosts'] and subnet != s:
                    G.add_edge(subnet, s)

            if interface["Interfaces"] == "IP Address" or "All":
                if visible not in s_hosts:
                    G.add_edge(s_host, visible, style='dashed', weight=0.25)

dashed_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('style') == 'dashed']
common_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('style') != 'dashed']

# deixa todos os hosts da mesma suberede com a mesma cor
colors = ['#484de8', '#48e8e3', '#65e848', '#e8e348', '#e85548']
pos = nx.spring_layout(G)
for subnet in subnets.keys():
    color = random.choice(colors)
    colors.remove(color)
    nodes = [u for u, d in G.nodes(data=True) if d.get('subnet') == subnet]
    nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=color, node_size=700, edgecolors='tab:gray')

nx.draw_networkx_edges(G, pos, edgelist=common_edges, edge_color='#1c1c1c', alpha=0.5)
nx.draw_networkx_edges(G, pos, edgelist=dashed_edges, style='dashed', edge_color='#1c1c1c', alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', font_family='monospace')

plt.show()
'''