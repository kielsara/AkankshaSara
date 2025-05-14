import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from config import *

def plot_spread_comparison(metrics):
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

def plot_belief_vs_share(metrics):
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

def visualize_h1_results(results):
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

def compare_variants(variant_metrics: dict):
    """
    variant_metrics = {
        'baseline': {'final_fake': 53, 'final_real': 18},
        'variant_A': {...},
        'variant_B': {...},
        ...
    }
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

def visualize_influencer_contribution(results_dict):
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

def visualize_h2_results(results_dict):
    compare_variants(results_dict)
    visualize_influencer_contribution(results_dict)
    print("\n[Belief vs Share for Fake News]")
    for key, res in results_dict.items():
        print(f"{key:<10} - Beliefs: {res['final_fake']:<4} | Shared: {res['shared_fake']:<4} | Share Rate: {res['shared_fake']/res['final_fake'] if res['final_fake'] else 0:.2f}")

def visualize_h3_results(results):
    print("\nBelief Revision Count:", results['belief_revised_count'])
    plot_belief_vs_share(results['metrics'])
