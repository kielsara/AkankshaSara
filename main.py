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


# Phase 2 logic - pending remove this comment
def initialize_p_shares(agents):
    for agent in agents.values():
        if agent.is_fact_checker:
            agent.p_share_fake = np.random.uniform(*p_fake_fact_checker)
        elif agent.is_susceptible:
            agent.p_share_fake = np.random.uniform(*p_fake_susceptible)
        else:
            agent.p_share_fake = np.random.uniform(*p_fake_normal)
        agent.p_share_real = np.random.uniform(*p_real_normal)


def select_initial_seeds(agents, news_type):
    seeds = random.sample(list(agents.keys()), seed_count)
    print(seeds)
    for uid in seeds:
        agents[uid].belief_state[news_type] = True
    return seeds


def schedule_initial_shares(seeds, agents, news_type, schedule):
    for uid in seeds:
        delay = random.randint(*fake_delay) if news_type == 'fake' else random.randint(*real_delay)
        schedule[delay].append((uid, news_type))


def simulate_spread(G, agents, news_items):
    schedule = defaultdict(list) #{ 7 :[ ( 1239, "real") ], 2 : [( 1100, "fake")]} Will get updated with initial seed numbers and then with neighbors
    stats = {'fake': [], 'real': []}
    infected = {'fake': set(), 'real': set()} #{ 'fake': (1100), 'real': (1239) }
    shared = {'fake': set(), 'real': set()} # { 'fake': (2) }

    for news_type in ['fake', 'real']:
        seeds = select_initial_seeds(agents, news_type)
        schedule_initial_shares(seeds, agents, news_type, schedule)
        infected[news_type].update(seeds)

    for round_num in range(max_rounds): # 50 rounds initially
        new_shares = {'fake': set(), 'real': set()}
        current_events = schedule.pop(round_num, [])

        for uid, news_type in current_events:
            agent = agents[uid]
            if agent.has_shared[news_type]:
                continue
            agent.has_shared[news_type] = True
            shared[news_type].add(uid)
            news_items[news_type].shared_count += 1

            for neighbor_id in G.neighbors(uid):
                neighbor = agents[neighbor_id]
                if neighbor.belief_state[news_type]: # check what needs to be done with the belief state, pending
                    continue
                trust = G[uid][neighbor_id]['trust']
                # if news_items[news_type].is_flagged_fake and news_type == 'fake': # Instead of halting further spread globally, reduce local trust for flagged fake news. - pending remove comment
                #     trust *= 0.3  # Cut effective trust, not transmission
                prob = agent.p_share_fake if news_type == 'fake' else agent.p_share_real
                effective_probability = prob * trust


                # if effective probability is below the threshold, news is not share by this neighbor and belief state is not changed
                if random.random() < effective_probability: # if the effective probability of sharing is greater than a random threshold, then share as per the below logic
                    # update this logic in the document - pending
                    if news_type == 'fake' and neighbor.is_fact_checker:
                        if random.random() < p_fact_check:  #choose a random number between 0.0 and 1.0(exclusive), if the random falls within 50% chance of fact-checking, news will be flagged if fake
                            news_items['fake'].flagged = True

                            continue
                    neighbor.belief_state[news_type] = True
                    infected[news_type].add(neighbor_id)
                    delay = random.randint(*(fake_delay if news_type == 'fake' else real_delay))
                    schedule[round_num + delay].append((neighbor_id, news_type))

        stats['fake'].append(len(infected['fake']))
        stats['real'].append(len(infected['real']))
        if not schedule:
            break

    return stats, infected, shared


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
#
# # Create news items
# fake_news = NewsItem("Bigfoot Sightings Up 200% This Year!", is_fake=True)
# real_news = NewsItem("NASA Confirms Water on Moon", is_fake=False)
#
# # Visualize the network
# visualize_network(G, agents)

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


# === Run Phase 2 Simulation ===


initialize_p_shares(agents)
for agent in agents.values():
    agent.belief_state = {'fake': False, 'real': False}
    agent.has_shared = {'fake': False, 'real': False}
news_items = {
    'fake': NewsItem("Bigfoot Sightings Up 200% This Year!", is_fake=True),
    'real': NewsItem("NASA Confirms Water on Moon", is_fake=False)
}
stats, infected, shared = simulate_spread(G, agents, news_items)
print("stats:",stats)

stats_summary = {
    "Final Fake News Reach": len(infected['fake']),
    "Final Real News Reach": len(infected['real']),
    "Total Fake Shares": (news_items['fake'].shared_count - seed_count ),
    "Total Real Shares": (news_items['real'].shared_count - seed_count),
    "Simulation Rounds Run": len(stats['fake'])
}
print(stats_summary)