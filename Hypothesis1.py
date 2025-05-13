import numpy as np
from config import *
from network_generator import create_social_network
from agent_initializer import assign_roles, assign_trust_levels
from simulation import initialize_p_shares, simulate_spread
from news_item import NewsItem


def hypothesis1(num_runs=1000):
    original_percent = percent_fact_checkers
    results = []

    # Test percentages to compare
    test_percentages = [0.1, 0.3, 0.5, 0.7, 0.8, 0.9, 1.0]

    for fc_pct in test_percentages:
        # Update global config
        new_percent_fc = fc_pct

        # Run simulations and collect metrics
        fake_reaches = []
        real_reaches = []

        for _ in range(num_runs):
            # Create new network/agents each run
            G = create_social_network(num_agents, num_communities, k_neighbors)
            agents = assign_roles(G,new_percent_fc)
            _ = assign_trust_levels(G, num_communities)
            initialize_p_shares(agents)

            # Initialize news items
            news_items = {
                'fake': NewsItem("Fake News", is_fake=True),
                'real': NewsItem("Real News", is_fake=False)
            }

            # Run simulation
            h1_stats, h1_infected, h1_shared, h1_final_beliefs, h1_belief_revised_count = simulate_spread(G, agents, news_items, hypothesis='h1')

            # Collect results
            fake_reaches.append(len(h1_infected['fake']))
            real_reaches.append(len(h1_infected['real']))

        # Store aggregated results
        results.append({
            'fc_percent': fc_pct,
            'avg_fake': np.mean(fake_reaches),
            'avg_real': np.mean(real_reaches),
            'std_fake': np.std(fake_reaches),
            'std_real': np.std(real_reaches)
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