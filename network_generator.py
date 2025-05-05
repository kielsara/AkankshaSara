'''
network_generator.py
'''

from config import *
import networkx as nx

# Create base graph with multiple communities

def create_social_network(num_agents, num_communities, k_neighbors):
    community_size = num_agents // num_communities
    G = nx.Graph()
    all_nodes = []

    for i in range(num_communities):
        ws = nx.watts_strogatz_graph(community_size, k_neighbors, rewire_fraction)
        mapping = {node: node + i * community_size for node in ws.nodes()}
        ws = nx.relabel_nodes(ws, mapping)
        G = nx.compose(G, ws)
        all_nodes.extend(ws.nodes()) # have node ids from 0 to 1499

    # Add long-range edges across communities (simulate scale-free hubs)
    ba = nx.barabasi_albert_graph(num_agents, ba_attachment)
    G.add_edges_from(ba.edges())

#Just for testing and debugging, remove it later or add Debug parameter - pending
    # for i, (node, data) in enumerate(G.nodes(data=True)):
    #     print(f"Node: {node}, Attributes: {data}")
    #     if i == 6:  # limit to first 10 nodes
    #         break
    #
    # for i, (u, v, data) in enumerate(G.edges(data=True)):
    #     print(f"Edge: {u} -- {v}, Attributes: {data}")
    #     if i == 6:  # limit to first 10 edges
    #         break
    #
    # print(list(G.nodes())[:6])  # first 10 node IDs
    # print(G.nodes[5])  # attributes of node with ID 5
    #
    return G
# --------------------------------------------------