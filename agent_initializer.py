import random
import numpy as np
from config import  *

# Define agent roles and properties
class Agent:
    def __init__(self, uid):
        self.id = uid
        self.is_influencer = False
        self.is_fact_checker = False
        self.is_susceptible = False
        self.number_of_friends = 0
        self.belief_state = False  # for given news item

# Assign roles to agents
def assign_roles(G):
    #Add comments here - pending
    agents = {}
    nodes = list(G.nodes())
    random.shuffle(nodes)

    num_influencers = int(influencer_fraction * num_agents)
    num_fact_checkers = int(fact_checker_fraction * num_agents)
    num_susceptible = int(susceptible_fraction * num_agents)

    influencers = set(nodes[:num_influencers])
    fact_checkers = set(nodes[num_influencers:num_influencers + num_fact_checkers])
    susceptibles = set(nodes[num_influencers + num_fact_checkers:
                             num_influencers + num_fact_checkers + num_susceptible])

    for node in nodes:
        agent = Agent(node)
        agent.is_influencer = node in influencers
        agent.is_fact_checker = node in fact_checkers
        agent.is_susceptible = node in susceptibles
        agent.number_of_friends = len(list(G.neighbors(node)))
        agents[node] = agent

    return agents

# Assign trust levels to edges
def assign_trust_levels(G, num_communities):
    community_labels = {}
    for i, node in enumerate(G.nodes()):
        community_labels[node] = i % num_communities

    for u, v in G.edges():
        if community_labels[u] == community_labels[v]:
            trust = np.random.uniform(0.7, 1.0) #intra-community
        else:
            trust = np.random.uniform(0.1, 0.4)  #inter-community
        G[u][v]['trust'] = trust

    return community_labels