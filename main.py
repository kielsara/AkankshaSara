'''
main.py
'''

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from collections import defaultdict
from typing import List
from typing import Dict, List, Tuple
from config import  *
from network_generator import *
from news_item import *
from agent_initializer import *


# Phase 2 logic - pending remove this comment
def initialize_p_shares(agents: Dict[int, Agent]):
    for agent in agents.values():
        if agent.is_fact_checker:
            agent.p_share_fake = np.random.uniform(*p_fake_fact_checker)
        elif agent.is_susceptible:
            if agent.susceptible_type == "super_spreader":
                agent.p_share_fake = np.random.uniform(*p_fake_super_spreader)
            elif agent.susceptible_type == "highly_susceptible":
                agent.p_share_fake = np.random.uniform(*p_fake_highly_susceptible)
            else:  # normal
                agent.p_share_fake = np.random.uniform(*p_fake_susceptible)
        else:
            agent.p_share_fake = np.random.uniform(*p_fake_normal)

        agent.p_share_real = np.random.uniform(*p_real_normal)


def select_initial_seeds(agents, news_type):
    seeds = random.sample(list(agents.keys()), seed_count)
    #print(seeds)
    for uid in seeds:
        agents[uid].belief_state = news_type
    return seeds


def sample_delay_from_distribution(delay_dist: Dict[int, float]) -> int:
    rand_val = random.random()
    cumulative = 0.0
    for delay, prob in sorted(delay_dist.items()):
        cumulative += prob
        if rand_val <= cumulative:
            return delay
    return max(delay_dist.keys())  # fallback in edge case


def schedule_initial_shares(seeds: List[int], agents: Dict[int, Agent], news_type: str, schedule: defaultdict):
    for uid in seeds:
        delay = sample_delay_from_distribution(
            fake_delay_distribution if news_type == 'fake' else real_delay_distribution
        )
        schedule[delay].append((uid, news_type))


def simulate_spread(G: nx.Graph, agents: Dict[int, Agent], news_items: Dict[str, NewsItem]) -> Tuple[Dict, Dict, Dict]:
    schedule = defaultdict(list) #{ 7 :[ ( 1239, "real") ], 2 : [( 1100, "fake")]} Will get updated with initial seed numbers and then with neighbors
    stats = {'fake': [], 'real': []}
    infected = {'fake': set(), 'real': set()} #{ 'fake': (1100), 'real': (1239) }
    shared = {'fake': set(), 'real': set()} # { 'fake': (2) }

    # Initialize seeds for both news types
    for news_type in ['fake', 'real']:
        seeds = select_initial_seeds(agents, news_type)
        schedule_initial_shares(seeds, agents, news_type, schedule)
        infected[news_type].update(seeds)

    # Run simulation rounds
    for round_num in range(max_rounds): # 500 rounds initially
        #new_shares = {'fake': set(), 'real': set()}
        current_events = schedule.pop(round_num, [])
        random.shuffle(current_events)  # Randomize processing order to avoid bias

        for uid, news_type in current_events:
            agent = agents[uid]
            if agent.has_shared[news_type]:
                continue
            agent.has_shared[news_type] = True
            shared[news_type].add(uid)
            news_items[news_type].shared_count += 1

            # Propagate to neighbors
            for neighbor_id in G.neighbors(uid):
                neighbor = agents[neighbor_id]
                # Check existing belief
                if neighbor.belief_state is not None:
                    continue  # Already believes something ( fake or real )

                # if neighbor.belief_state[news_type]: # check what needs to be done with the belief state, pending
                #     continue

                trust = G[uid][neighbor_id]['trust']
                # if news_items[news_type].is_flagged_fake and news_type == 'fake': # Instead of halting further spread globally, reduce local trust for flagged fake news. - pending remove comment
                #     trust *= 0.3  # Cut effective trust, not transmission
                prob = agent.p_share_fake if news_type == 'fake' else agent.p_share_real
                effective_probability = prob * trust


                # if effective probability is below the threshold, news is not share by this neighbor and belief state is not changed
                if random.random() < effective_probability: # if the effective probability of sharing is greater than a random threshold, then share as per the below logic
                    # update this logic in the document - pending
                    # Fact-checker intervention
                    if news_type == 'fake' and neighbor.is_fact_checker:
                        if random.random() < p_fact_check:  #choose a random number between 0.0 and 1.0(exclusive), if the random falls within 50% chance of fact-checking, news will be flagged if fake
                            news_items['fake'].flagged = True
                            continue # fact-checkers won't share the news further, halting the spread entirely for this neighbor's path

                    # Commit to believe current news if currently belief state is False for both the news_type
                    neighbor.belief_state = news_type
                    infected[news_type].add(neighbor_id)
                    delay = sample_delay_from_distribution(
                        fake_delay_distribution if news_type == 'fake' else real_delay_distribution
                    )
                    schedule[round_num + delay].append((neighbor_id, news_type))

        stats['fake'].append(len(infected['fake']))
        stats['real'].append(len(infected['real']))
        if not schedule:
            break

    return stats, infected, shared

# Metrics Collection for baseline (10,000) Runs
def run_baseline_simulation(num_runs: int = 1000) -> Dict[str, List]: # comment above says 10k but this defaults to 1k? - pending
    metrics = {
        'fake_reach': [], 'real_reach': [],
        'fake_peak_round': [], 'real_peak_round': [],
        'fake_shares': [], 'real_shares': []
    }

    for _ in range(num_runs):
        # Re-initialize network and agents for each run
        G = create_social_network(num_agents, num_communities, k_neighbors)
        agents = assign_roles(G)
        trust_levels_communities = assign_trust_levels(G, num_communities)
        initialize_p_shares(agents)

        # Reset agent belief states and shared status
        for agent in agents.values():
            agent.belief_state = None
            agent.has_shared = {'fake': False, 'real': False}

        # Initialize news items
        news_items = {
            'fake': NewsItem("Fake News", is_fake=True), #give some meaningful news title here - pending
            'real': NewsItem("Real News", is_fake=False)
        }

        # Run simulation
        stats, infected, shared = simulate_spread(G, agents, news_items)

        # Record metrics
        metrics['fake_reach'].append(len(infected['fake']))
        metrics['real_reach'].append(len(infected['real']))
        metrics['fake_shares'].append(news_items['fake'].shared_count)
        metrics['real_shares'].append(news_items['real'].shared_count)
        metrics['fake_peak_round'].append(np.argmax(np.diff(stats['fake'])))
        metrics['real_peak_round'].append(np.argmax(np.diff(stats['real'])))

    return metrics

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


def plot_baseline_results(metrics: Dict[str, List]):
    plt.figure(figsize=(12, 6))

    # Reach Comparison
    plt.subplot(2, 2, 1)
    plt.hist(metrics['fake_reach'], bins=50, alpha=0.5, label='Fake')
    plt.hist(metrics['real_reach'], bins=50, alpha=0.5, label='Real')
    plt.title("Final Reach Distribution")
    plt.xlabel("Number of Infected Agents")
    plt.legend()

    # Sharing Activity
    plt.subplot(2, 2, 2)
    plt.scatter(metrics['fake_reach'], metrics['fake_shares'], alpha=0.1)
    plt.title("Fake News: Reach vs Shares")
    plt.xlabel("Reach"), plt.ylabel("Shares")

    # Peak Timing
    plt.subplot(2, 2, 3)
    plt.hist(metrics['fake_peak_round'], bins=30, alpha=0.5, label='Fake')
    plt.hist(metrics['real_peak_round'], bins=30, alpha=0.5, label='Real')
    plt.title("Peak Spread Timing")
    plt.xlabel("Simulation Round")
    plt.legend()

    plt.tight_layout()
    plt.savefig('baseline_results.png')
    plt.show()


# Generate the network
# G = create_social_network(num_agents, num_communities, k_neighbors)
# agents = assign_roles(G)
# community_labels = assign_trust_levels(G, num_communities)
# #
# # # Create news items
# # fake_news = NewsItem("Bigfoot Sightings Up 200% This Year!", is_fake=True)
# # real_news = NewsItem("NASA Confirms Water on Moon", is_fake=False)
# #
# # # Visualize the network
# # visualize_network(G, agents)
#
# # Output some summary stats for confirmation
# summary = {
#     "Total Agents": num_agents,
#     "Influencers": sum(1 for a in agents.values() if a.is_influencer),
#     "Fact Checkers": sum(1 for a in agents.values() if a.is_fact_checker),
#     "Susceptible": sum(1 for a in agents.values() if a.is_susceptible),
#     "Normal Users": sum(1 for a in agents.values() if not (a.is_influencer or a.is_fact_checker or a.is_susceptible)),
#     "Total Edges": G.number_of_edges()
# }
# print(summary)


# # === Run Phase 2 Simulation ===
#
#
# initialize_p_shares(agents)
# for agent in agents.values():
#     agent.belief_state = {'fake': False, 'real': False}
#     agent.has_shared = {'fake': False, 'real': False}
# news_items = {
#     'fake': NewsItem("Bigfoot Sightings Up 200% This Year!", is_fake=True),
#     'real': NewsItem("NASA Confirms Water on Moon", is_fake=False)
# }
# stats, infected, shared = simulate_spread(G, agents, news_items)
# print("stats:",stats)
#
# stats_summary = {
#     "Final Fake News Reach": len(infected['fake']),
#     "Final Real News Reach": len(infected['real']),
#     "Total Fake Shares": (news_items['fake'].shared_count - seed_count ),
#     "Total Real Shares": (news_items['real'].shared_count - seed_count),
#     "Simulation Rounds Run": len(stats['fake'])
# }
# print(stats_summary)


# Main Execution
if __name__ == "__main__":
    num_runs = 1000
    baseline_metrics = run_baseline_simulation(num_runs)
    plot_baseline_results(baseline_metrics)

    #print metrics
    #print(baseline_metrics)
    # Print summary statistics
    print(f"\nBaseline Statistics ({num_runs:,} runs):")
    print(f"Fake News - Avg Reach: {np.mean(baseline_metrics['fake_reach']):.1f} ± {np.std(baseline_metrics['fake_reach']):.1f}")
    print(f"Real News - Avg Reach: {np.mean(baseline_metrics['real_reach']):.1f} ± {np.std(baseline_metrics['real_reach']):.1f}")
    print(f"Fake Peak Round: {np.median(baseline_metrics['fake_peak_round'])} (IQR {np.percentile(baseline_metrics['fake_peak_round'], 25)}-{np.percentile(baseline_metrics['fake_peak_round'], 75)})")
    print(f"Real Peak Round: {np.median(baseline_metrics['real_peak_round'])} (IQR {np.percentile(baseline_metrics['real_peak_round'], 25)}-{np.percentile(baseline_metrics['real_peak_round'], 75)})")