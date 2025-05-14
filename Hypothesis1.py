import numpy as np
from baseline_run import run_baseline_simulation

def run_hypothesis1_experiment(fact_checker_variants, num_runs=1000):

    results = []

    for fc_pct in fact_checker_variants:

        h1_metrics, h1_belief_revised_count = run_baseline_simulation(num_runs, hypothesis='h1', percent_fc=fc_pct)

        # Collect results
        final_reach_fake = [run[-1] for run in h1_metrics['fake_reach'] if len(run) > 0]
        final_reach_real = [run[-1] for run in h1_metrics['real_reach'] if len(run) > 0]

        print("\n")
        print(f"H1 Results when fact-checker percent is {fc_pct}:")
        print(f"Average number of fake news shares: {np.mean(h1_metrics['fake_shares']):.1f} ± {np.std(h1_metrics['fake_shares']):.1f}")
        print(f"Average number of real news shares: {np.mean(h1_metrics['real_shares']):.1f}± {np.std(h1_metrics['real_shares']):.1f}")
        print(f"Fake News - Avg Reach: {np.mean(final_reach_fake):.1f} ± {np.std(final_reach_fake):.1f}")
        print(f"Real News - Avg Reach: {np.mean(final_reach_real):.1f} ± {np.std(final_reach_real):.1f}")
        # Store aggregated results
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


