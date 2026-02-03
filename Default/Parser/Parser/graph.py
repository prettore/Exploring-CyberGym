import matplotlib.pyplot as plt
import networkx as nx
G = nx.DiGraph()

#def add_router():

#def add_host(router):

p1,p2,p3 = (-2,0,2)
pos = {
    "Router1": (p1,0),
    "Router2": (p2,0),
    "Router3": (p3,0),
    "User0": (p1,0.5),
    "User1": (p1,-0.5),
    "User2": (p1-1,-0.25),
    "User3": (p1-1,0.25),
    "Enterprise0": (p2-0.5, 0.5),
    "Enterprise1": (p2-0.5, -0.5),
    "Enterprise2": (p2+0.5, 0.5),
    "Velo_Server": (p2+0.5, -0.5),
    "Op_Host0": (p3,0.5),
    "Op_Host1": (p3,-0.5),
    "Op_Host2": (p3+1,-0.25),
    "Op_Server0": (p3+1,0.25),
}

G = nx.Graph()
G.add_nodes_from(pos.keys())
G.add_edge("Router1","Router2")
G.add_edge("Router2","Router3")

G.add_edge("Router1","User0")
G.add_edge("Router1","User1")
G.add_edge("Router1","User2")
G.add_edge("Router1","User3")

G.add_edge("Router2","Enterprise0")
G.add_edge("Router2","Enterprise1")
G.add_edge("Router2","Enterprise2")
G.add_edge("Router2","Velo_Server")

G.add_edge("Router3","Op_Host0")
G.add_edge("Router3","Op_Host1")
G.add_edge("Router3","Op_Host2")
G.add_edge("Router3","Op_Server0")

nx.draw(G, pos, with_labels=True)
plt.show()
