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