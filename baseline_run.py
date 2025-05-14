
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from collections import defaultdict
from typing import List, Dict, List, Tuple, Any, Set
#from typing import Dict, List, Tuple
from config import  *
from network_generator import *
from news_item import *
from agent_initializer import *
from simulation import simulate_spread, initialize_p_shares


# Metrics Collection for baseline (1,000) Runs
def run_baseline_simulation(num_runs: int = 1000, hypothesis=None, percent_fc=percent_fact_checkers) -> tuple[
    dict[str | Any, list[Any] | Any], int | Any]:
    stats = {'fake': [], 'real': []}
    belief_revised_count = 0
    metrics = {
        'fake_reach': [], 'real_reach': [],
        'fake_peak_round': [], 'real_peak_round': [],
        'fake_shares': [], 'real_shares': [],
        'fake_belief_count': [], 'real_belief_count': [],
        'influencer_counts_fake': [], 'influencer_counts_real': [],
        'influencer_total_fake': [], 'influencer_total_real': []
    }

    #move this to h2
    # influencer_counts = {'fake': 0, 'real': 0}
    # influencer_total = {'fake': 0, 'real': 0}

    for run_num in range(num_runs):
        # Re-initialize network and agents for each run
        G = create_social_network(num_agents, num_communities, k_neighbors)
        agents = assign_roles(G,percent_fc=percent_fc)
        assign_trust_levels(G, num_communities)
        initialize_p_shares(agents)

        # Reset agent belief states and shared status
        for agent in agents.values():
            agent.belief_state = None
            agent.has_shared = {'fake': False, 'real': False}

        # Initialize news items
        news_items = {
            'fake': NewsItem("Fake News", is_fake=True),
            'real': NewsItem("Real News", is_fake=False)
        }

        # Run simulation for others
        stats, final_beliefs, belief_revised_count = simulate_spread(G, agents, news_items, hypothesis=None)

        #move this to h2.py file
        # if hypothesis == 'h2':
        #     influencer_counts, influencer_total = trace_influencer_paths(G, agents, news_items, infected)
        #     metrics['influencer_counts_fake'].append(influencer_counts['fake'])
        #     metrics['influencer_counts_real'].append(influencer_counts['real'])
        #     metrics['influencer_total_fake'].append(influencer_total['fake'])
        #     metrics['influencer_total_real'].append(influencer_total['real'])

        # Record metrics
        metrics['fake_reach'].append(stats['fake'])
        metrics['real_reach'].append(stats['real'])
        metrics['fake_shares'].append(news_items['fake'].shared_count)
        metrics['real_shares'].append(news_items['real'].shared_count)
        metrics['fake_peak_round'].append(np.argmax(np.diff(stats['fake'])) if len(stats['fake']) > 1 else 0)
        metrics['real_peak_round'].append(np.argmax(np.diff(stats['real'])) if len(stats['real']) > 1 else 0)
        metrics['fake_belief_count'].append((final_beliefs['fake']))
        metrics['real_belief_count'].append((final_beliefs['real']))

    return metrics, belief_revised_count
