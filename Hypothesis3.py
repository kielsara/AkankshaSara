import numpy as np
from baseline_run import run_baseline_simulation


def run_hypothesis3(real_news_delay):

    h3_metrics, h3_belief_revised_counts= run_baseline_simulation(num_runs=1000, hypothesis='h3',real_news_delay=real_news_delay)

    final_reach_fake = [run[-1] for run in h3_metrics['fake_reach'] if len(run) > 0]
    final_reach_real = [run[-1] for run in h3_metrics['real_reach'] if len(run) > 0]

    print("\n")
    print(f"H3 Results with a delay of {real_news_delay} rounds :")
    print(f"Average number of fake news shares: {np.mean(h3_metrics['fake_shares']):.1f} ± {np.std(h3_metrics['fake_shares']):.1f}")
    print(f"Average number of real news shares: {np.mean(h3_metrics['real_shares']):.1f}± {np.std(h3_metrics['real_shares']):.1f}")
    print(f"Fake News - Avg Reach: {np.mean(final_reach_fake):.1f} ± {np.std(final_reach_fake):.1f}")
    print(f"Real News - Avg Reach: {np.mean(final_reach_real):.1f} ± {np.std(final_reach_real):.1f}")
    print(f"Fake News Avg Believers : {np.mean(h3_metrics['fake_belief_count']):.1f} ± {np.std(h3_metrics['fake_belief_count']):.1f}")
    print(f"Real News Avg Believers: {np.mean(h3_metrics['real_belief_count']):.1f} ± {np.std(h3_metrics['real_belief_count']):.1f}")

    # Collect results
    results = {
        'metrics': h3_metrics,
        'belief_revised_count': np.mean(h3_belief_revised_counts)
    }

    return results


