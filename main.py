'''
main.py
'''

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
import pandas as pd
from simulation import simulate_spread, initialize_p_shares
from metrics import plot_belief_vs_share, plot_spread_comparison, visualize_h1_results, visualize_h2_results, visualize_h3_results
from collections import deque
from baseline_run import run_baseline_simulation
from Hypothesis1 import run_hypothesis1_experiment
from hypothesis2 import run_all_variants
from Hypothesis3 import run_hypothesis3

#move all viz to metrics file

#
# def plot_baseline_results(metrics: Dict[str, List]):
#     plt.figure(figsize=(12, 6))
#
#     # Reach Comparison
#     plt.subplot(2, 2, 1)
#     plt.hist(metrics['fake_reach'], bins=50, alpha=0.5, label='Fake')
#     plt.hist(metrics['real_reach'], bins=50, alpha=0.5, label='Real')
#     plt.title("Final Reach Distribution")
#     plt.xlabel("Number of Infected Agents")
#     plt.legend()
#
#     # Sharing Activity
#     plt.subplot(2, 2, 2)
#     plt.scatter(metrics['fake_reach'], metrics['fake_shares'], alpha=0.1)
#     plt.title("Fake News: Reach vs Shares")
#     plt.xlabel("Reach"), plt.ylabel("Shares")
#
#     # Peak Timing
#     plt.subplot(2, 2, 3)
#     plt.hist(metrics['fake_peak_round'], bins=30, alpha=0.5, label='Fake')
#     plt.hist(metrics['real_peak_round'], bins=30, alpha=0.5, label='Real')
#     plt.title("Peak Spread Timing")
#     plt.xlabel("Simulation Round")
#     plt.legend()
#
#     plt.tight_layout()
#     plt.savefig('baseline_results.png')
#     plt.show()
#

# Main Execution
if __name__ == "__main__":
    # baseline is below
    num_runs = 1000

#---------------------- commenting it to avoid late running issue ---------
    # print("--- Running Baseline ---")
    # baseline_metrics, base_belief_revised_count = run_baseline_simulation(num_runs, hypothesis=None)
    #
    # final_reach_fake = [run[-1] for run in baseline_metrics['fake_reach'] if len(run) > 0]
    #
    # final_reach_real = [run[-1] for run in baseline_metrics['real_reach'] if len(run) > 0]
    #
    #
    # print("\nBaseline Results:")
    # #print(f"Average number of fake news believers: {np.mean(baseline_metrics['fake_belief_count']):.1f} ± {np.std(baseline_metrics['fake_belief_count']):.1f}")
    # #print(f"Average number of real news believers: {np.mean(baseline_metrics['real_belief_count']):.1f} ± {np.std(baseline_metrics['real_belief_count']):.1f}")
    # print(f"Average number of fake news shares: {np.mean(baseline_metrics['fake_shares']):.1f} ± {np.std(baseline_metrics['fake_shares']):.1f}")
    # print(f"Average number of real news shares: {np.mean(baseline_metrics['real_shares']):.1f}± {np.std(baseline_metrics['real_shares']):.1f}")
    # print(f"Fake News - Avg Reach: {np.mean(final_reach_fake):.1f} ± {np.std(final_reach_fake):.1f}")
    # print(f"Real News - Avg Reach: {np.mean(final_reach_real):.1f} ± {np.std(final_reach_real):.1f}")
    # #plot spread across 1000 runs for the baseline
    # plot_spread_comparison(baseline_metrics)
    # # plot a comparison between  total beliefs vs total shares for fake news
    # # plot_belief_vs_share(baseline_metrics)
    #
    # print("\n--- Running Hypothesis 1: Impact of having more fact-checkers in the network ---")
    # fact_checker_variants = [0.5, 0.7, 0.9]
    # h1_results = run_hypothesis1_experiment(fact_checker_variants=fact_checker_variants)
    # visualize_h1_results(h1_results)

    print("\n--- Running Hypothesis 2: Influencer Behavior Variants ---")
    h2_results = run_all_variants()
    visualize_h2_results(h2_results)

    # -----------------------

    print("\n--- Running Hypothesis 3: Competitive Interference ---")
    h3_results = run_hypothesis3(real_news_delay=3)
    visualize_h3_results(h3_results)





    # Print summary statistics
    # def print_metrics(metrics, label, num_runs):
    #     print(f"\n{label} Statistics ({num_runs:,} runs):")
    #     print(f"Fake News - Avg Reach: {np.mean(metrics['fake_reach']):.1f} ± {np.std(metrics['fake_reach']):.1f}")
    #     print(f"Real News - Avg Reach: {np.mean(metrics['real_reach']):.1f} ± {np.std(metrics['real_reach']):.1f}")
    #     print(f"Fake Peak Round: {np.median(metrics['fake_peak_round'])} (IQR {np.percentile(metrics['fake_peak_round'], 25)}-{np.percentile(metrics['fake_peak_round'], 75)})")
    #     print(f"Real Peak Round: {np.median(metrics['real_peak_round'])} (IQR {np.percentile(metrics['real_peak_round'], 25)}-{np.percentile(metrics['real_peak_round'], 75)})")
        # print(f"Fake Final Believers: {np.mean(h3_metrics['fake_belief_count']):.1f} ± {np.std(h3_metrics['fake_belief_count']):.1f}")
        # print(f"Real Final Believers: {np.mean(h3_metrics['real_belief_count']):.1f} ± {np.std(h3_metrics['real_belief_count']):.1f}")
        # print(f"Influencer Counts Fake: {np.mean(h2_metrics['influencer_counts_fake']):.1f} ± {np.std(h2_metrics['influencer_counts_fake']):.1f}")
        # print(f"Influencer Counts Real: {np.mean(h2_metrics['influencer_counts_real']):.1f} ± {np.std(h2_metrics['influencer_counts_real']):.1f}")
        # print(f"Influencer Total Fake: {np.mean(h2_metrics['influencer_total_fake']):.1f} ± {np.std(h2_metrics['influencer_total_fake']):.1f}")
        # print(f"Influencer Total Real: {np.mean(h2_metrics['influencer_total_real']):.1f} ± {np.std(h2_metrics['influencer_total_real']):.1f}")
        #

    # Print metrics
    # print_metrics(baseline_metrics, "Baseline", num_runs)
    # print_metrics(h3_metrics, "Hypothesis 3", num_runs)

