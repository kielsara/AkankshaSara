'''
agent_initializer.py
'''

import random
import numpy as np
from collections import defaultdict
import statistics
from config import  *


# Define agent roles and properties
class Agent:
    def __init__(self, uid):
        self.id = uid
        self.is_influencer = False
        self.is_fact_checker = False
        self.is_susceptible = False
        self.susceptible_type = None  # 'normal', 'highly_susceptible', 'super_spreader'
        self.number_of_friends = 0
        self.belief_state = None #(None/'fake'/'real')
        self.has_shared = {'fake': False, 'real': False}
        self.p_share_fake = 0.0
        self.p_share_real = 0.0


def assign_roles(G):
    agents = {}

    # Top-level role counts
    num_influencers = int(percent_influencers * num_agents)
    num_skeptical = int(percent_skeptical * num_agents)
    num_fact_checkers = int(percent_fact_checkers * num_skeptical)
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

    # validating that influencers have highest degrees, can convert this to debug - pending
    # Collect degrees by agent type
    # degree_stats = defaultdict(list)
    #
    # for node, agent in agents.items():
    #     deg = agent.number_of_friends
    #     if agent.is_influencer:
    #         degree_stats['influencer'].append(deg)
    #     elif agent.is_fact_checker:
    #         degree_stats['fact_checker'].append(deg)
    #     elif agent.is_susceptible:
    #         degree_stats[f'susceptible_{agent.susceptible_type}'].append(deg)
    #     else:
    #         degree_stats['normal'].append(deg)
    #
    # print("\n Degree Stats by Agent Type:")
    # for role, degs in degree_stats.items():
    #     print(f"{role:<25} count={len(degs):<4} mean={statistics.mean(degs):.2f}  max={max(degs)}  min={min(degs)}")

    return agents


# Assign trust levels to edges
def assign_trust_levels(G, num_communities):
    community_labels = {}
    for i, node in enumerate(G.nodes()):
        community_labels[node] = i % num_communities

    for u, v in G.edges():
        if community_labels[u] == community_labels[v]:
            trust = np.random.uniform(0.6, 1.0) #intra-community
        else:
            trust = np.random.uniform(0.1, 0.4)  #inter-community
        G[u][v]['trust'] = trust

    return community_labels