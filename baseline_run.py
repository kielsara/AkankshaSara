'''
baseline_run.py

This module defines the core function for running the baseline simulation for this project.
It performs multiple Monte Carlo trials (typically 1000) and collects performance metrics
to benchmark against variant hypotheses.

Each run independently initializes a network, assigns agent roles and behaviors, seeds both news types,
and simulates diffusion dynamics under configured parameters. Outputs include belief counts, peak rounds,
share counts, and attribution of spread origin (influencer vs. regular user).

This script is intended to be called from main.py or hypothesis experiments for controlled testing.
'''

from typing import List, Dict, List, Tuple, Any, Set
from config import  *
from network_generator import *
from news_item import *
from agent_initializer import *
from simulation import simulate_spread, initialize_p_shares

# Metrics Collection for baseline (1,000) Runs
def run_baseline_simulation(num_runs: int = 1000, hypothesis: str | None = None, percent_fc: float = percent_fact_checkers,
    variant_flag: Dict[str, bool] = variant_config, real_news_delay: int = 0) -> Tuple[Dict[str, List[Any]], int]:
    """
    Executes multiple Monte Carlo simulation runs using default parameters
    to establish a baseline for spread dynamics.

    Parameters:
        num_runs : int. Number of simulation runs to perform.
        hypothesis : str or None. Optional hypothesis label ('h2', 'h3') for variant configuration.
        percent_fc : float. Proportion of skeptical agents designated as fact-checkers.
        variant_flag : dict. Flags enabling variant features (e.g., influencer control, trust boost).
        real_news_delay : int. Number of rounds to delay the real news release (used in Hypothesis 3).

    Returns:
        metrics : dict. Dictionary containing time-series and aggregate metrics across runs.
        belief_revised_counts : list. List of belief revision counts per run.

    Examples:
        >>> results, revisions = run_baseline_simulation(num_runs=5)
        >>> isinstance(results, dict)
        True
        >>> 'fake_reach' in results and 'real_shares' in results
        True
        >>> isinstance(revisions, list)
        True
    """
    stats = {'fake': [], 'real': []}
    belief_revised_counts = []
    metrics = {
        'fake_reach': [], 'real_reach': [],
        'fake_peak_round': [], 'real_peak_round': [],
        'fake_shares': [], 'real_shares': [],
        'fake_belief_count': [], 'real_belief_count': [],
        'influencer_reach_fake': [], 'normal_reach_fake': []
    }

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
        stats, final_beliefs, belief_revised_count, influencer_impact = simulate_spread(G, agents, news_items, hypothesis=hypothesis, variant_flag_dict=variant_flag, real_news_delay=real_news_delay)

        # Record metrics
        metrics['fake_reach'].append(stats['fake'])
        metrics['real_reach'].append(stats['real'])
        metrics['fake_shares'].append(news_items['fake'].shared_count)
        metrics['real_shares'].append(news_items['real'].shared_count)
        metrics['fake_peak_round'].append(np.argmax(np.diff(stats['fake'])) + 1 if len(stats['fake']) > 1 else 0)
        metrics['real_peak_round'].append(np.argmax(np.diff(stats['real'])) + 1 if len(stats['real']) > 1 else 0)
        metrics['fake_belief_count'].append((final_beliefs['fake']))
        metrics['real_belief_count'].append((final_beliefs['real']))
        metrics['influencer_reach_fake'].append(influencer_impact['influencer'])
        metrics['normal_reach_fake'].append(influencer_impact['normal'])

        belief_revised_counts.append(belief_revised_count)

    return metrics, belief_revised_counts