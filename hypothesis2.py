'''
hypothesis2.py

This module defines simulation variants used to test Hypothesis 2, which investigates
how different influencer behaviors affect the spread of misinformation. Each variant
enables a combination of control flags:
- Variant A: Seed influencers more heavily.
- Variant B: Give influencers a speed advantage.
- Variant C: Boost trust in influencer-shared content.

Each variant is run using shared simulation logic, and results are aggregated for
comparison across key metrics.
'''

import numpy as np
from baseline_run import run_baseline_simulation

def run_variant(name: str, variant_flags: dict, hypothesis: str = 'h2') -> tuple[str, dict]:
    """
    Executes a single variant run under Hypothesis 2 and collects key metrics.

    Parameters:
        name : str. Label for the variant (e.g., 'variant_AB').
        variant_flags : dict. Flags controlling which influencer mechanisms are enabled.
        hypothesis : str. Optional hypothesis label, defaults to 'h2'.

    Returns:
        tuple : tuple. Variant label and a dictionary of outcome metrics.

    Examples:
        >>> flags = {'variant_A': True, 'variant_B': False, 'variant_C': False}
        >>> name, result = run_variant('variant_A', flags)
        >>> 'final_fake' in result and 'shared_fake' in result
        True
    """
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


def run_all_variants() -> dict:
    """
    Executes all defined influencer behavior variants and aggregates results.

    Returns:
        dict : dict. Dictionary mapping variant name to its outcome metrics.

    Examples:
        >>> results = run_all_variants() # doctest: +SKIP
        >>> 'variant_ABC' in results and 'final_real' in results['variant_ABC'] # doctest: +SKIP
        True
    """
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