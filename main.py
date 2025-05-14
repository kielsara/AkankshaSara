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


# Main Execution
if __name__ == "__main__":
    # baseline is below
    num_runs = 1000

    print("--- Running Baseline ---")
    baseline_metrics, base_belief_revised_count = run_baseline_simulation(num_runs, hypothesis=None)

    final_reach_fake = [run[-1] for run in baseline_metrics['fake_reach'] if len(run) > 0]
    final_reach_real = [run[-1] for run in baseline_metrics['real_reach'] if len(run) > 0]

    print("\nBaseline Results:")

    print(f"Fake News - Avg Reach: {np.mean(final_reach_fake):.1f} ± {np.std(final_reach_fake):.1f}")
    print(f"Real News - Avg Reach: {np.mean(final_reach_real):.1f} ± {np.std(final_reach_real):.1f}")
    print(f"Fake Peak Round: {np.median(baseline_metrics['fake_peak_round'])} (IQR {np.percentile(baseline_metrics['fake_peak_round'], 25)}-{np.percentile(baseline_metrics['fake_peak_round'], 75)})")
    print(f"Real Peak Round: {np.median(baseline_metrics['real_peak_round'])} (IQR {np.percentile(baseline_metrics['real_peak_round'], 25)}-{np.percentile(baseline_metrics['real_peak_round'], 75)})")

    #plot spread across 1000 runs for the baseline
    plot_spread_comparison(baseline_metrics)

    print("\n--- Running Hypothesis 1: Impact of having more fact-checkers in the network ---")
    fact_checker_variants = [0.5, 0.7, 0.9]
    h1_results = run_hypothesis1_experiment(fact_checker_variants=fact_checker_variants)
    visualize_h1_results(h1_results)

    print("\n--- Running Hypothesis 2: Influencer Behavior Variants ---")
    h2_results = run_all_variants()
    visualize_h2_results(h2_results)

    print("\n--- Running Hypothesis 3: Competitive Interference with delay---")
    h3_results = run_hypothesis3(real_news_delay=3)
    visualize_h3_results(h3_results)