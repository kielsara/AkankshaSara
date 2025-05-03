import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from collections import defaultdict
from typing import List
from config import  *
from network_generator import *
from news_item import *
from agent_initializer import *


# Visualize network
def visualize_network(G, agents, title='Social Network Graph'):
    color_map = []
    for node in G:
        agent = agents[node]
        if agent.is_influencer:
            color_map.append('green')
        elif agent.is_fact_checker:
            color_map.append('blue')
        elif agent.is_susceptible:
            color_map.append('red')
        else:
            color_map.append('gray')

    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, node_color=color_map, with_labels=False, node_size=30, edge_color='lightgray')
    plt.title(title)
    plt.show()


# Generate the network
G = create_social_network(num_agents, num_communities, k_neighbors)
agents = assign_roles(G)
community_labels = assign_trust_levels(G, num_communities)

# Create news items
fake_news = NewsItem("Bigfoot Sightings Up 200% This Year!", is_fake=True)
real_news = NewsItem("NASA Confirms Water on Moon", is_fake=False)

# Visualize the network
visualize_network(G, agents)

# Output some summary stats for confirmation
summary = {
    "Total Agents": num_agents,
    "Influencers": sum(1 for a in agents.values() if a.is_influencer),
    "Fact Checkers": sum(1 for a in agents.values() if a.is_fact_checker),
    "Susceptible": sum(1 for a in agents.values() if a.is_susceptible),
    "Normal Users": sum(1 for a in agents.values() if not (a.is_influencer or a.is_fact_checker or a.is_susceptible)),
    "Total Edges": G.number_of_edges()
}
print(summary)