import numpy as np
from config import *
from network_generator import create_social_network
from agent_initializer import assign_roles, assign_trust_levels
from simulation import initialize_p_shares, simulate_spread
from news_item import NewsItem
from baseline_run import run_baseline_simulation

def run_variant(name: str, variant_flags: dict, hypothesis: str = 'h2'):

    # Set global config for variant
   # variant_config.update(variant_flags)
    #influencer_stats = []

    h2_metrics, h2_belief_revised_count = run_baseline_simulation(num_runs=1000, hypothesis=hypothesis, variant_flag=variant_flags)

    # Collect results
    final_reach_fake = [run[-1] for run in h2_metrics['fake_reach'] if len(run) > 0]
    final_reach_real = [run[-1] for run in h2_metrics['real_reach'] if len(run) > 0]
    print("\n")
    print(f"H2 Results for {name}:")
    print(f"Average number of fake news shares: {np.mean(h2_metrics['fake_shares']):.1f} ± {np.std(h2_metrics['fake_shares']):.1f}")
    print(f"Average number of real news shares: {np.mean(h2_metrics['real_shares']):.1f}± {np.std(h2_metrics['real_shares']):.1f}")
    print(f"Fake News - Avg Reach: {np.mean(final_reach_fake):.1f} ± {np.std(final_reach_fake):.1f}")
    print(f"Real News - Avg Reach: {np.mean(final_reach_real):.1f} ± {np.std(final_reach_real):.1f}")

    # Store aggregated results
    result = {
        'final_fake': np.mean(h2_metrics['fake_belief_count']),
        'final_real': np.mean(h2_metrics['real_belief_count']),
        'shared_fake': np.mean(h2_metrics['fake_shares']),
        'shared_real': np.mean(h2_metrics['real_shares']),
        'inf_origin_fake': np.mean(h2_metrics['influencer_counts_fake']),
        'inf_origin_real': np.mean(h2_metrics['influencer_counts_real']),
        'inf_total_fake': np.mean(h2_metrics['influencer_total_fake']),
        'inf_total_real': np.mean(h2_metrics['influencer_total_real']),
    }
    return name, result


def run_all_variants():
    variants = {
        'baseline': {'variant_A': False, 'variant_B': False, 'variant_C': False},
        #'variant_A': {'variant_A': True, 'variant_B': False, 'variant_C': False},
        # 'variant_B': {'variant_A': False, 'variant_B': True, 'variant_C': False},
        # 'variant_C': {'variant_A': False, 'variant_B': False, 'variant_C': True},
        'variant_ABC': {'variant_A': True, 'variant_B': True, 'variant_C': True},
    }

    all_results = {}
    for name, flags in variants.items():
        label, data = run_variant(name, flags)
        all_results[label] = data

    return all_results