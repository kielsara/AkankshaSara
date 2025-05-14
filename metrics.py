'''
metrics.py

This module contains functions for visualizing and comparing results
from simulations.

It includes:
- Boxplots and bar charts for final reach and belief vs. share counts
- Line plots for Hypothesis 1 (fact-checker efficacy)
- Bar comparisons for Hypothesis 2 variants (influencer behaviors)
- Belief revision and sharing patterns for Hypothesis 3 (competing news dynamics)

These visualizations help interpret outcomes from Monte Carlo trials
and support analysis across different experimental setups.
'''

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List

def plot_spread_comparison(metrics: Dict[str, List[List[int]]]) -> None:
    """
    Plots a boxplot comparing the final number of agents reached by fake and real news.
    This boxplot is specifically used to visualize baseline simulation results.

    Parameters:
        metrics : dict. Dictionary containing 'fake_reach' and 'real_reach' lists (per round per run).

    Returns:
        None

    Examples:
        >>> metrics = {'fake_reach': [[0, 50], [0, 55]], 'real_reach': [[0, 20], [0, 25]]}
        >>> plot_spread_comparison(metrics)  # displays a boxplot
    """
    # Extract final reach from each run (last element of each round stats)
    final_reach_fake = [run[-1] for run in metrics['fake_reach'] if len(run) > 0]
    final_reach_real = [run[-1] for run in metrics['real_reach'] if len(run) > 0]

    plt.figure(figsize=(7, 5))
    plt.boxplot([final_reach_fake, final_reach_real], labels=['Fake', 'Real'])
    plt.ylabel('Final Number of Reached Agents')
    plt.title('Final Spread Comparison Across 1000 Simulations')
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


def plot_belief_vs_share(metrics: Dict[str, List[float]]) -> None:
    """
    Plots a bar chart comparing average belief counts and share counts for fake and real news.
    This bar chart is specifically used to visualize Hypothesis 3 results.

    Parameters:
        metrics : dict. Dictionary with 'fake_belief_count', 'real_belief_count', 'fake_shares', and 'real_shares' lists across simulation runs.

    Returns:
        None

    Examples:
        >>> metrics = {'fake_belief_count': [50], 'real_belief_count': [20],
        ...            'fake_shares': [45], 'real_shares': [18]}
        >>> plot_belief_vs_share(metrics)  # displays a bar chart
    """
    types = ['fake', 'real']
    beliefs = [np.mean(metrics['fake_belief_count']), np.mean(metrics['real_belief_count'])]
    shares = [np.mean(metrics['fake_shares']), np.mean(metrics['real_shares'])]

    x = np.arange(len(types))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width/2, beliefs, width, label='Mean Belief Count', color='skyblue')
    ax.bar(x + width/2, shares, width, label='Mean Share Count', color='salmon')
    ax.set_xticks(x)
    ax.set_xticklabels(['Fake', 'Real'])
    ax.set_ylabel('Agent Count')
    ax.set_title('Belief vs Share Counts (1000 Runs)')
    ax.legend()
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()


def visualize_h1_results(results: List[Dict[str, float]]) -> None:
    """
    Plots average news reach for fake and real news as the percentage of fact-checkers increases.
    As the name suggests, this plot is used for visualizing Hypothesis 1 results.

    Parameters:
        results : list of dict. Each dict must have 'fc_percent', 'fake_mean', and 'real_mean' keys.

    Returns:
        None

    Examples:
        >>> results = [{'fc_percent': 10, 'fake_mean': 50, 'real_mean': 20}]
        >>> visualize_h1_results(results)  # displays a line plot
    """
    x = [r['fc_percent'] for r in results]
    fake_y = [r['fake_mean'] for r in results]
    real_y = [r['real_mean'] for r in results]

    plt.figure(figsize=(10, 5))
    plt.plot(x, fake_y, label='Fake News Reach', marker='o')
    plt.plot(x, real_y, label='Real News Reach', marker='s')
    plt.xlabel('% Fact-Checkers')
    plt.ylabel('Average Reach')
    plt.title('Impact of Fact-Checker Percentage on News Reach')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def compare_variants(variant_metrics: Dict[str, Dict[str, float]]) -> None:
    """
    Compares final belief counts across different simulation variants using a grouped bar chart.
    This plot is specifically used to visualize Hypothesis 2 results.

    Parameters:
    variant_metrics : dict. Dictionary with variant names as keys and dicts of 'final_fake' and 'final_real' as values.

    Returns:
        None

    Examples:
        >>> variant_metrics = {'baseline': {'final_fake': 50, 'final_real': 20},
        ...                    'variant_A': {'final_fake': 40, 'final_real': 25}}
        >>> compare_variants(variant_metrics)  # displays bar chart
    """
    categories = list(variant_metrics.keys())
    fake_vals = [variant_metrics[k]['final_fake'] for k in categories]
    real_vals = [variant_metrics[k]['final_real'] for k in categories]

    x = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - width/2, fake_vals, width, label='Fake News')
    ax.bar(x + width/2, real_vals, width, label='Real News')

    ax.set_ylabel('Final Belief Count')
    ax.set_title('Final Beliefs: Baseline vs Variants')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()

    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()


def visualize_influencer_contribution(results_dict: Dict[str, Dict[str, List[float]]]) -> None:
    """
    Creates a bar chart comparing the average fake news reach initiated by influencers vs. regular users.
    This visualization is specifically used to visualize Hypothesis 2 results.

    Parameters:
        results_dict : dict. Dictionary containing 'influencer_reach_fake' and 'normal_reach_fake' per variant.

    Returns:
        None

    Examples:
        >>> results_dict = {'variant_A': {'influencer_reach_fake': [30], 'normal_reach_fake': [20]}}
        >>> visualize_influencer_contribution(results_dict)  # displays grouped bars
    """
    categories = list(results_dict.keys())
    for category in categories:
        if category == 'baseline' or category == 'variant_BC':
            del categories[categories.index(category)]

    influencer_vals = [np.mean(results_dict[k]['influencer_reach_fake']) for k in categories]
    normal_vals = [np.mean(results_dict[k]['normal_reach_fake']) for k in categories]

    x = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - width/2, influencer_vals, width, label='Influencer-Originated')
    ax.bar(x + width/2, normal_vals, width, label='Normal-Originated')

    ax.set_ylabel('Avg Reach (Fake News)')
    ax.set_title('Influencer vs Normal Spread Impact (Hypothesis 2)')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()


def visualize_h2_results(results_dict: Dict[str, Dict[str, float]]) -> None:
    """
    Displays charts and prints belief/share rates for fake news under Hypothesis 2 variants.
    As the name suggests, these charts and prints are used for visualizing Hypothesis 2 results.

    Parameters:
        results_dict : dict. Dictionary where each key is a variant and each value includes final_fake, shared_fake.

    Returns:
        None

    Examples:
        >>> results_dict = {
        ...     'variant_A': {
        ...         'final_fake': 50, 'final_real': 20,
        ...         'shared_fake': 40,
        ...         'influencer_reach_fake': [30],
        ...         'normal_reach_fake': [20]
        ...     }
        ... }
        >>> visualize_h2_results(results_dict)  # doctest: +SKIP
    """
    compare_variants(results_dict)
    visualize_influencer_contribution(results_dict)
    print("\n[Belief vs Share for Fake News]")
    for key, res in results_dict.items():
        print(f"{key:<10} - Beliefs: {res['final_fake']:<4} | Shared: {res['shared_fake']:<4} | Share Rate: {res['shared_fake']/res['final_fake'] if res['final_fake'] else 0:.2f}")


def visualize_h3_results(results: Dict[str, any]) -> None:
    """
    Calls plot_belief_vs_share() and prints belief revision count from Hypothesis 3 testing.

    Parameters:
        results : dict. Dictionary with 'belief_revised_count' and 'metrics' (must include share/belief data).

    Returns:
        None

    Examples:
        >>> results = {'belief_revised_count': 10,
        ...            'metrics': {'fake_belief_count': [50], 'real_belief_count': [20],
        ...                        'fake_shares': [45], 'real_shares': [18]}}
        >>> visualize_h3_results(results)  # doctest: +SKIP
    """
    print("\nBelief Revision Count:", results['belief_revised_count'])
    plot_belief_vs_share(results['metrics'])