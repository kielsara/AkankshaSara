import numpy as np
from config import *
from network_generator import create_social_network
from agent_initializer import assign_roles, assign_trust_levels
from simulation import initialize_p_shares, simulate_spread
from news_item import NewsItem
from metrics import plot_belief_vs_share
from baseline_run import run_baseline_simulation


def run_hypothesis3(real_news_delay):


    h3_metrics, h3_belief_revised_counts= run_baseline_simulation(num_runs=1000, hypothesis='h3',real_news_delay=real_news_delay)


    results = {
        'metrics': h3_metrics,
        #'shared': shared,
        #'beliefs': final_beliefs,
        'belief_revised_count': np.mean(h3_belief_revised_counts)
        #'infected': infected
    }

    return results


