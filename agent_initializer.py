'''
agent_initializer.py

This module defines the Agent class and provides functions to initialize
agents with roles and behavioral parameters, as well as assign trust levels
on a social network graph. These roles support the simulation of information
diffusion, belief change, and social influence.

Roles include:
- Influencers (high connectivity, high impact)
- Fact-checkers (can flag fake news)
- Susceptible users (more likely to believe/share misinformation)
- Regular users (default behavior)

Trust levels are assigned to edges based on community affiliation,
with intra-community connections receiving higher trust.
'''

import random
import numpy as np
from config import  *
import networkx as nx
from typing import Dict

# Define agent roles and properties
class Agent:
    """
    Represents an individual node/user in the social network with a role and behavior profile.

    Attributes:
        id : int. Node identifier.
        is_influencer : bool. Whether the agent is an influencer.
        is_fact_checker : bool. Whether the agent can flag fake news.
        is_susceptible : bool. Whether the agent is more vulnerable to misinformation.
        susceptible_type : str or None. One of 'normal', 'highly_susceptible', 'super_spreader'.
        number_of_friends : int. Number of direct neighbors in the graph.
        belief_state : str or None. Current belief ('fake', 'real', or None).
        has_shared : dict. Tracks whether the agent has shared each news type.
        p_share_fake : float. Probability of sharing fake news.
        p_share_real : float. Probability of sharing real news.
    """
    def __init__(self, uid: int):
        self.id = uid
        self.is_influencer = False
        self.is_fact_checker = False
        self.is_susceptible = False
        self.susceptible_type = None
        self.number_of_friends = 0
        self.belief_state = None
        self.has_shared = {'fake': False, 'real': False}
        self.p_share_fake = 0.0
        self.p_share_real = 0.0


def assign_roles(G: nx.Graph, percent_fc: float = percent_fact_checkers) -> Dict[int, Agent]:
    """
    Assigns roles to agents in the graph based on network structure and predefined proportions.

    Parameters:
        G : nx.Graph. Social network graph.
        percent_fc : float. Percentage of skeptical users assigned as fact-checkers.

    Returns:
        Dict[int, Agent]: Mapping of node IDs to Agent instances.

    Examples:
        >>> import networkx as nx
        >>> G = nx.erdos_renyi_graph(100, 0.05)
        >>> agents = assign_roles(G)
        >>> len(agents) == 100
        True
    """
    agents = {}

    # Top-level role counts
    num_influencers = int(percent_influencers * num_agents)
    num_skeptical = int(percent_skeptical * num_agents)
    num_fact_checkers = int(percent_fc * num_skeptical)
    num_susceptible = int(percent_susceptible * num_agents)

    # Rank nodes by degree (descending)
    sorted_nodes_by_degree = sorted(G.degree(), key=lambda x: x[1], reverse=True)
    sorted_nodes = [node for node, _ in sorted_nodes_by_degree]

    # Influencers are highest degree nodes
    influencers = set(sorted_nodes[:num_influencers])

    # Shuffle all nodes for other role assignments
    random.shuffle(sorted_nodes)

    fact_checkers = set(sorted_nodes[:num_fact_checkers])
    susceptible_pool = sorted_nodes[num_fact_checkers:num_fact_checkers + num_susceptible]
    susceptibles = set(susceptible_pool)

    # Susceptible subgroup counts
    num_super_spreaders = max(1, int(percent_super_spreader * num_susceptible))
    num_highly_susceptible = random.randint(
        int(percent_highly_susceptible_range[0] * num_susceptible),
        int(percent_highly_susceptible_range[1] * num_susceptible)
    )
    num_normal_susceptible = num_susceptible - num_highly_susceptible - num_super_spreaders

    random.shuffle(susceptible_pool)
    super_spreaders = set(susceptible_pool[:num_super_spreaders])
    highly_susceptible = set(susceptible_pool[num_super_spreaders:
                                              num_super_spreaders + num_highly_susceptible])
    normal_susceptibles = set(susceptible_pool[num_super_spreaders + num_highly_susceptible:])

    # Assign properties to each agent
    for node in G.nodes():
        agent = Agent(node)
        agent.is_influencer = node in influencers
        agent.is_fact_checker = node in fact_checkers
        agent.is_susceptible = node in susceptibles
        agent.number_of_friends = len(list(G.neighbors(node)))

        if agent.is_susceptible:
            if node in super_spreaders:
                agent.susceptible_type = 'super_spreader'
            elif node in highly_susceptible:
                agent.susceptible_type = 'highly_susceptible'
            else:
                agent.susceptible_type = 'normal'

        agents[node] = agent
    return agents


# Assign trust levels to edges
def assign_trust_levels(G: nx.Graph, num_communities: int) -> Dict[int, int]:
    """
    Assigns trust values to edges in the network based on community affiliation.
    Intra-community edges receive high trust (0.8–1.0), inter-community edges lower trust (0.1–0.5).

    Parameters:
        G : nx.Graph. Graph with nodes and edges.
        num_communities : int. Number of modular communities assumed.

    Returns:
        Dict[int, int]: Mapping of node ID to community label.

    Examples:
        >>> G = nx.path_graph(10)
        >>> labels = assign_trust_levels(G, num_communities=2)
        >>> isinstance(labels, dict)
        True
        >>> all(0 <= v < 2 for v in labels.values())
        True
    """
    community_labels = {}
    for i, node in enumerate(G.nodes()):
        community_labels[node] = i % num_communities

    for u, v in G.edges():
        if community_labels[u] == community_labels[v]:
            trust = np.random.uniform(0.8, 1.0) # intra-community
        else:
            trust = np.random.uniform(0.1, 0.5) # inter-community
        G[u][v]['trust'] = trust

    return community_labels