'''
network_generator.py

This module defines the function used to create the synthetic social network structure
in all simulation scenarios. The generated network structure
mimics real-world online platforms by combining:

- Watts-Strogatz (WS) small-world graphs to form clustered communities.
- Barabási–Albert (BA) graphs to add scale-free, long-range connections across communities.

The resulting hybrid network supports simulation of information diffusion,
influence dynamics, and community-based behaviors.

Key Features:
- Adjustable number of agents, communities, and local connectivity.
- Optional debug mode to inspect node and edge structure.
'''

from config import *
import networkx as nx

def create_social_network(num_agents: int, num_communities: int, k_neighbors: int, debug: bool = False) -> nx.Graph:
    """
    Creates a synthetic hybrid social network by combining multiple small-world
    communities (Watts-Strogatz) with global scale-free connectivity (Barabási–Albert).

    The result mimics real-world social platforms: high clustering within local communities
    and long-range influence via central hubs.

    Parameters:
        num_agents : int. Total number of agents (nodes) in the network.
        num_communities : int. Number of community clusters to divide the network into.
        k_neighbors : int. Each node is connected to k nearest neighbors in ring topology (used in Watts-Strogatz model).
        debug : bool, optional. If True, prints out sample node and edge attributes for debugging (default is False).

    Returns:
        nx.Graph : A NetworkX graph representing the synthetic social network.

    Examples:
        >>> G = create_social_network(150, 3, 4)
        >>> isinstance(G, nx.Graph)
        True
        >>> len(G)  # Number of nodes
        150
        >>> nx.number_connected_components(G) == 1  # Should be one connected network
        True
    """
    community_size = num_agents // num_communities
    G = nx.Graph()
    all_nodes = []

    for i in range(num_communities):
        ws = nx.watts_strogatz_graph(community_size, k_neighbors, rewire_fraction)
        mapping = {node: node + i * community_size for node in ws.nodes()}
        ws = nx.relabel_nodes(ws, mapping)
        G = nx.compose(G, ws)
        all_nodes.extend(ws.nodes())

    # Add long-range edges across communities (simulate scale-free hubs)
    ba = nx.barabasi_albert_graph(num_agents, ba_attachment)
    G.add_edges_from(ba.edges())

    if debug:
        print("Debug: Sample node data")
        for i, (node, data) in enumerate(G.nodes(data=True)):
            print(f"Node: {node}, Attributes: {data}")
            if i == 6:
                break

        print("\nDebug: Sample edge data")
        for i, (u, v, data) in enumerate(G.edges(data=True)):
            print(f"Edge: {u} -- {v}, Attributes: {data}")
            if i == 6:
                break

        print("\nDebug: Sample node IDs and attributes")
        print(list(G.nodes())[:6])
        if 5 in G.nodes:
            print(G.nodes[5])

    return G