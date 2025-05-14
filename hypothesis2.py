import numpy as np
from baseline_run import run_baseline_simulation

def run_variant(name: str, variant_flags: dict, hypothesis: str = 'h2'):

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

    if variant_flags['variant_A']:
        print(f"\n{name} - Influencer Impact when variant A - Increasing the number of initial influencer seeds")
        print(f"Avg reach of fake news from influencers: {np.mean(h2_metrics['influencer_reach_fake']):.1f} ± {np.std(h2_metrics['influencer_reach_fake']):.1f}")
        print(f"Avg reach of fake news from normal users: {np.mean(h2_metrics['normal_reach_fake']):.1f} ± {np.std(h2_metrics['normal_reach_fake']):.1f}")

    # Store aggregated results
    result = {
        'final_fake': np.mean(h2_metrics['fake_belief_count']),
        'final_real': np.mean(h2_metrics['real_belief_count']),
        'shared_fake': np.mean(h2_metrics['fake_shares']),
        'shared_real': np.mean(h2_metrics['real_shares']),
        'influencer_reach_fake': h2_metrics['influencer_reach_fake'],
        'normal_reach_fake': h2_metrics['normal_reach_fake']
    }
    return name, result


def run_all_variants():
    variants = {
        'baseline': {'variant_A': False, 'variant_B': False, 'variant_C': False},
        'variant_AB': {'variant_A': True, 'variant_B': True, 'variant_C': False},
        'variant_BC': {'variant_A': False, 'variant_B': True, 'variant_C': True},
        'variant_CA': {'variant_A': True, 'variant_B': False, 'variant_C': True},
        'variant_ABC': {'variant_A': True, 'variant_B': True, 'variant_C': True},
    }

    all_results = {}
    for name, flags in variants.items():
        label, data = run_variant(name, flags)
        all_results[label] = data

    return all_results