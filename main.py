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
import pandas as pd


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


def schedule_initial_shares(seeds, agents, news_type, schedule, delay_offset=0):
    for uid in seeds:
        delay = sample_delay_from_distribution(
            fake_delay_distribution if news_type == 'fake' else real_delay_distribution
        )
        schedule[delay + delay_offset].append((uid, news_type))


def simulate_spread(G: nx.Graph, agents: Dict[int, Agent], news_items: Dict[str, NewsItem], is_h3=False, real_news_delay=0) -> Tuple[Dict, Dict, Dict]:
    schedule = defaultdict(list) #{ 7 :[ ( 1239, "real") ], 2 : [( 1100, "fake")]} Will get updated with initial seed numbers and then with neighbors
    stats = {'fake': [], 'real': []}
    infected = {'fake': set(), 'real': set()} #{ 'fake': (1100), 'real': (1239) }
    shared = {'fake': set(), 'real': set()} # { 'fake': (2) }
    belief_revised_count = 0

    # Initialize seeds for both news types
    for news_type in ['fake', 'real']:
        if news_type == 'real' and is_h3:
            delay_round = real_news_delay
        else:
            delay_round = 0
        seeds = select_initial_seeds(agents, news_type)
        schedule_initial_shares(seeds, agents, news_type, schedule, delay_round)
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
                # if neighbor.belief_state is not None:
                #     continue  # Already believes something ( fake or real )

                if neighbor.belief_state is not None:
                    if is_h3 and neighbor.belief_state != news_type and neighbor.is_fact_checker:
                        if random.random() < p_belief_revision:
                            neighbor.belief_state = news_type
                            infected[news_type].add(neighbor_id)
                            belief_revised_count += 1
                            delay = sample_delay_from_distribution(
                                real_delay_distribution if news_type == 'real' else fake_delay_distribution
                            )
                            schedule[round_num + delay].append((neighbor_id, news_type))
                    continue

                trust = G[uid][neighbor_id]['trust']
                if news_type == 'fake' and news_items['fake'].is_flagged_fake:
                    trust *= 0.3  # Reduce trust for flagged fake news
                prob = agent.p_share_fake if news_type == 'fake' else agent.p_share_real
                effective_probability = prob * trust


                # if effective probability is below the threshold, news is not share by this neighbor and belief state is not changed
                if random.random() < effective_probability: # if the effective probability of sharing is greater than a random threshold, then share as per the below logic
                    # Fact-checker intervention
                    if news_type == 'fake' and neighbor.is_fact_checker:
                        if random.random() < p_fact_check:  #choose a random number between 0.0 and 1.0(exclusive), if the random falls within 50% chance of fact-checking, news will be flagged if fake
                            news_items['fake'].flagged = True
                            #continue # fact-checkers won't share the news further, halting the spread entirely for this neighbor's path

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

    final_beliefs = {'fake': 0, 'real': 0}
    for agent in agents.values():
        if agent.belief_state == 'fake':
            final_beliefs['fake'] += 1
        elif agent.belief_state == 'real':
            final_beliefs['real'] += 1

    return stats, infected, shared, final_beliefs, belief_revised_count


# Metrics Collection for baseline (1,000) Runs
def run_baseline_simulation(num_runs: int = 1000, is_h3=False) -> Tuple[Dict[str, List], Dict[str, Dict[str, float]]]:

    metrics = {
        'fake_reach': [], 'real_reach': [],
        'fake_peak_round': [], 'real_peak_round': [],
        'fake_shares': [], 'real_shares': [],
        'fake_belief_count': [], 'real_belief_count': []
    }


    for run_num in range(num_runs):
        # Re-initialize network and agents for each run
        G = create_social_network(num_agents, num_communities, k_neighbors)
        agents = assign_roles(G)
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

        # Run simulation
        stats, infected, shared, final_beliefs, belief_revised_count = simulate_spread(G, agents, news_items)

        # Record metrics
        metrics['fake_reach'].append(len(infected['fake']))
        metrics['real_reach'].append(len(infected['real']))
        metrics['fake_shares'].append(news_items['fake'].shared_count)
        metrics['real_shares'].append(news_items['real'].shared_count)
        metrics['fake_peak_round'].append(np.argmax(np.diff(stats['fake'])) if len(stats['fake']) > 1 else 0)
        metrics['real_peak_round'].append(np.argmax(np.diff(stats['real'])) if len(stats['real']) > 1 else 0)
        metrics['fake_belief_count'].append((final_beliefs['fake']))
        metrics['real_belief_count'].append((final_beliefs['real']))

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


# =================== hypothesis 1 testing code ======================
def test_hypothesis1(num_runs=1000):
    original_percent = percent_fact_checkers
    results = []

    # Test percentages to compare
    test_percentages = [0.1, 0.3, 0.5, 0.8]

    for fc_pct in test_percentages:
        # Update global config
        globals()['percent_fact_checkers'] = fc_pct

        # Run simulations and collect metrics
        fake_reaches = []
        real_reaches = []

        for _ in range(num_runs):
            # Create new network/agents each run
            G = create_social_network(num_agents, num_communities, k_neighbors)
            agents = assign_roles(G)
            _ = assign_trust_levels(G, num_communities)
            initialize_p_shares(agents)

            # Initialize news items
            news_items = {
                'fake': NewsItem("Fake News", is_fake=True),
                'real': NewsItem("Real News", is_fake=False)
            }

            # Run simulation
            stats, infected, shared, role_infection = simulate_spread(G, agents, news_items)

            # Collect results
            fake_reaches.append(len(infected['fake']))
            real_reaches.append(len(infected['real']))

        # Store aggregated results
        results.append({
            'fc_percent': fc_pct,
            'avg_fake': np.mean(fake_reaches),
            'avg_real': np.mean(real_reaches),
            'std_fake': np.std(fake_reaches),
            'std_real': np.std(real_reaches)
        })

    # Restore original value
    globals()['percent_fact_checkers'] = original_percent

    # Print results
    print("\nHypothesis 1 Results:")
    print("| Fact-Checkers % | Avg Fake Reach | Avg Real Reach |")
    print("|-----------------|----------------|----------------|")
    for res in results:
        print(
            f"| {res['fc_percent'] * 100:>14.0f}% | {res['avg_fake']:>13.1f} ± {res['std_fake']:.1f} | {res['avg_real']:>13.1f} ± {res['std_real']:.1f} |")

    return results


# Main Execution
if __name__ == "__main__":
    # baseline is below
    num_runs = 1000
    # baseline_metrics = run_baseline_simulation(num_runs, is_h3=True)
    # plot_baseline_results(baseline_metrics)

    baseline_metrics = run_baseline_simulation(num_runs, is_h3=False)
    h3_metrics = run_baseline_simulation(num_runs, is_h3=True)

    # Print summary statistics
    def print_metrics(metrics, label, num_runs):
        print(f"\n{label} Statistics ({num_runs:,} runs):")
        print(f"Fake News - Avg Reach: {np.mean(metrics['fake_reach']):.1f} ± {np.std(metrics['fake_reach']):.1f}")
        print(f"Real News - Avg Reach: {np.mean(metrics['real_reach']):.1f} ± {np.std(metrics['real_reach']):.1f}")
        print(f"Fake Peak Round: {np.median(metrics['fake_peak_round'])} (IQR {np.percentile(metrics['fake_peak_round'], 25)}-{np.percentile(metrics['fake_peak_round'], 75)})")
        print(f"Real Peak Round: {np.median(metrics['real_peak_round'])} (IQR {np.percentile(metrics['real_peak_round'], 25)}-{np.percentile(metrics['real_peak_round'], 75)})")
        print(f"Fake Final Believers: {np.mean(metrics['fake_belief_count']):.1f} ± {np.std(metrics['fake_belief_count']):.1f}")
        print(f"Real Final Believers: {np.mean(metrics['real_belief_count']):.1f} ± {np.std(metrics['real_belief_count']):.1f}")

    # Print metrics
    print_metrics(baseline_metrics, "Baseline", num_runs)
    print_metrics(h3_metrics, "Hypothesis 3", num_runs)

    # test_hypothesis1(num_runs=100)