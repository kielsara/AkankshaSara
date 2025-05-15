'''
main.py

This is the primary execution script for running the full misinformation simulation framework.
It sequentially runs baseline and experimental simulations, collects metrics, and visualizes results
to evaluate three core hypotheses.

Execution Flow:
1. Baseline Simulation:
   - Runs the default misinformation and factual news spread across 1000 trials.
   - Reports average reach, peak rounds, and variability.

2. Hypothesis 1:
   - Tests the impact of increasing the percentage of fact-checkers in the network.
   - Visualizes how spread is reduced as fact-checker density increases.

3. Hypothesis 2:
   - Explores influencer behavior and role in the spread (Variants A, B, C).
   - Tracks how influencer-seeded misinformation differs from baseline.

4. Hypothesis 3:
   - Introduces competing factual news after a delay to test belief revision.
   - Reports belief switches and comparative reach dynamics.

Output includes summary statistics and plots to support analysis of misinformation dynamics.
'''

from agent_initializer import *
from metrics import plot_belief_vs_share, plot_spread_comparison, visualize_h1_results, visualize_h2_results, visualize_h3_results
from baseline_run import run_baseline_simulation
from hypothesis1 import run_hypothesis1_experiment
from hypothesis2 import run_all_variants
from hypothesis3 import run_hypothesis3


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

    # plot spread across 1000 runs for the baseline
    plot_spread_comparison(baseline_metrics)

    # hypothesis 1 is below
    print("\n--- Running Hypothesis 1: Impact of having more fact-checkers in the network ---")
    fact_checker_variants = [0.5, 0.7, 0.9]
    h1_results = run_hypothesis1_experiment(fact_checker_variants=fact_checker_variants)
    visualize_h1_results(h1_results)

    # hypothesis 2 is below
    print("\n--- Running Hypothesis 2: Influencer Behavior Variants ---")
    h2_results = run_all_variants()
    visualize_h2_results(h2_results)

    # hypothesis 3 is below
    print("\n--- Running Hypothesis 3: Competitive Interference with delay---")
    h3_results = run_hypothesis3(real_news_delay=3)
    visualize_h3_results(h3_results)