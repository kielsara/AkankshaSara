import matplotlib.pyplot as plt
import numpy as np
from config import *


# def pad_with_nan(metrics_data, max_len):
#     '''
#     Need to pad the data in metrics['fake_reach'] with nan because length of each list in metrics['fake_reach']
#     is not the same as for each simulation spread can die out at different round number between 1 and 500
#     '''
#     padded_data = []
#     for run in metrics_data:
#         if len(run) == 0:
#             continue  # Skip empty runs
#         padded_run = list(run) + [np.nan] * (max_len - len(run))
#         padded_data.append(padded_run)
#     return np.array(padded_data)

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

def visualize_h2_results(results_dict):
    compare_variants(results_dict)

    print("\n[Belief vs Share for Fake News]")
    for key, res in results_dict.items():
        print(f"{key:<10} - Beliefs: {res['final_fake']:<4} | Shared: {res['shared_fake']:<4} | Share Rate: {res['shared_fake']/res['final_fake'] if res['final_fake'] else 0:.2f}")


# --- New Visualization for Hypothesis 2 ---
def visualize_influencer_impact(stats, influencer_data):
    plt.figure(figsize=(10, 5))

    # Line Plot of Cumulative Spread
    plt.plot(stats['fake'], label='Fake (Cumulative)')
    plt.plot(stats['real'], label='Real (Cumulative)')
    plt.title("Cumulative Spread Over Time")
    plt.xlabel("Round")
    plt.ylabel("Number of Believing Agents")
    plt.legend()
    plt.show()

    # Bar Plot: Influencer Reach Ratio
    fake_ratio = influencer_data['fake'] / stats['fake'][-1]
    real_ratio = influencer_data['real'] / stats['real'][-1]
    plt.bar(['Fake', 'Real'], [fake_ratio, real_ratio], color=['orange', 'green'])
    plt.title("% Reach from Influencer-Originated Spread")
    plt.ylabel("Ratio")
    plt.show()



def visualize_h3_results(results):
    print("\nBelief Revision Count:", results['belief_revised_count'])
    plot_spread_comparison(results['metrics'])
    plot_belief_vs_share(results['metrics'])

#Visualize network
# def visualize_network(G, agents, title='Social Network Graph'):
#     color_map = []
#     for node in G:
#         agent = agents[node]
#         if agent.is_influencer:
#             color_map.append('green')
#         elif agent.is_fact_checker:
#             color_map.append('blue')
#         elif agent.is_susceptible:
#             color_map.append('red')
#         else:
#             color_map.append('gray')
#
#     plt.figure(figsize=(12, 10))
#     pos = nx.spring_layout(G, seed=42)
#     nx.draw(G, pos, node_color=color_map, with_labels=False, node_size=30, edge_color='lightgray')
#     plt.title(title)
#     plt.show()
# #