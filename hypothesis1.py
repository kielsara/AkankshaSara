'''
hypothesis1.py

This module defines the experimental routine for Hypothesis 1, which tests the impact
of increasing the proportion of fact-checkers in a social network on the spread of fake
and real news. The experiment is conducted by varying the fact-checker percentage and
collecting outcome metrics across multiple simulation runs.

Returns aggregated statistics used for analysis and visualization.
'''

import numpy as np
from baseline_run import run_baseline_simulation

def run_hypothesis1_experiment(fact_checker_variants: list[float], num_runs: int = 1000) -> list[dict]:
    """
    Runs simulation for varying percentages of fact-checkers and returns reach metrics.

    Parameters:
        fact_checker_variants : list of float. List of percentages of skeptical users to assign as fact-checkers.
        num_runs : int. Number of simulation runs per configuration.

    Returns:
        list of dict. Each dict contains aggregated results for a fact-checker configuration.

    Examples:
        >>> results = run_hypothesis1_experiment([0.1, 0.3], num_runs=5) # doctest: +SKIP
        >>> isinstance(results, list) and 'fc_percent' in results[0] # doctest: +SKIP
        True
    """
    results = []

    for fc_pct in fact_checker_variants:
        h1_metrics, h1_belief_revised_count = run_baseline_simulation(
            num_runs, hypothesis='h1', percent_fc=fc_pct)

        final_reach_fake = [run[-1] for run in h1_metrics['fake_reach'] if len(run) > 0]
        final_reach_real = [run[-1] for run in h1_metrics['real_reach'] if len(run) > 0]

        print("\n")
        print(f"H1 Results when fact-checker percent is {fc_pct}:")
        print(f"Average number of fake news shares: {np.mean(h1_metrics['fake_shares']):.1f} ± {np.std(h1_metrics['fake_shares']):.1f}")
        print(f"Average number of real news shares: {np.mean(h1_metrics['real_shares']):.1f}± {np.std(h1_metrics['real_shares']):.1f}")
        print(f"Fake News - Avg Reach: {np.mean(final_reach_fake):.1f} ± {np.std(final_reach_fake):.1f}")
        print(f"Real News - Avg Reach: {np.mean(final_reach_real):.1f} ± {np.std(final_reach_real):.1f}")

        results.append({
            'fc_percent': fc_pct,
            'fake_mean': np.mean(final_reach_fake),
            'fake_std': np.std(final_reach_fake),
            'real_mean': np.mean(final_reach_real),
            'real_std': np.std(final_reach_real),
            'fake_all': final_reach_fake,
            'real_all': final_reach_real
        })

    return results