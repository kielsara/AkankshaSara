import numpy as np
from config import *
from network_generator import create_social_network
from agent_initializer import assign_roles, assign_trust_levels
from simulation import initialize_p_shares, simulate_spread
from news_item import NewsItem
from baseline_run import run_baseline_simulation
import matplotlib.pyplot as plt


def run_hypothesis1_experiment(fact_checker_variants, num_runs=1000):
    #original_percent = percent_fact_checkers
    results = []

    # Test percentages to compare
    #test_percentages = [0.1, 0.3, 0.5, 0.7, 0.8, 0.9, 1.0]

    for fc_pct in fact_checker_variants:
        # Update global config
        #new_percent_fc = fc_pct

        # Run simulations and collect metrics
        # fake_reaches = []
        # real_reaches = []

        h1_metrics, h1_belief_revised_count = run_baseline_simulation(num_runs, hypothesis=None, percent_fc=fc_pct)

        # Collect results
        final_reach_fake = [run[-1] for run in h1_metrics['fake_reach'] if len(run) > 0]
        final_reach_real = [run[-1] for run in h1_metrics['real_reach'] if len(run) > 0]

        # for _ in range(num_runs):
        #     # Create new network/agents each run
        #     G = create_social_network(num_agents, num_communities, k_neighbors)
        #     agents = assign_roles(G,percent_fc=fc_pct)
        #     _ = assign_trust_levels(G, num_communities)
        #     initialize_p_shares(agents)
        #
        #     # Reset agent belief states and shared status
        #     for agent in agents.values():
        #         agent.belief_state = None
        #         agent.has_shared = {'fake': False, 'real': False}
        #
        #     # Initialize news items
        #     news_items = {
        #         'fake': NewsItem("Fake News", is_fake=True),
        #         'real': NewsItem("Real News", is_fake=False)
        #     }
        #
        #     # Run simulation
        #     h1_stats, h1_infected, h1_shared, h1_final_beliefs, h1_belief_revised_count = simulate_spread(G, agents, news_items, hypothesis='h1')

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

    # # Restore original value
    # globals()['percent_fact_checkers'] = original_percent
    #
    # # Print results
    # print("\nHypothesis 1 Results:")
    # print("| Fact-Checkers % | Avg Fake Reach | Avg Real Reach |")
    # print("|-----------------|----------------|----------------|")
    # for res in results:
    #     print(f"| {res['fc_percent'] * 100:>14.0f}% | {res['avg_fake']:>13.1f} ± {res['std_fake']:.1f} | {res['avg_real']:>13.1f} ± {res['std_real']:.1f} |")

    return results

def visualize_h1_results(results):
    x = [r['fc_percent'] for r in results]
    fake_y = [r['fake_mean'] for r in results]
    real_y = [r['real_mean'] for r in results]

    plt.figure(figsize=(10, 5))
    plt.plot(x, fake_y, label='Fake News Reach', marker='o')
    plt.plot(x, real_y, label='Real News Reach', marker='s')
    plt.xlabel('% Fact-Checkers')
    plt.ylabel('Average Reach')
    plt.title('Impact of Fact-Checker Percentage on News Reach')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
