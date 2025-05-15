'''
config.py

This module centralizes all global constants and parameter settings used throughout
the project. It allows easy experimentation and reproducibility by separating configuration from logic.

Key Configuration Areas:
- Simulation size and runtime limits (e.g., number of agents, max rounds)
- Role distributions (e.g., influencers, fact-checkers, susceptible users)
- News sharing probabilities (for fake and real news, based on user type)
- Fact-checker intervention rates and belief revision behavior
- Delay distributions for news propagation
- Variant toggles for Hypothesis 2 experiments
- Network structure parameters (e.g., community count, rewiring probability)

This modular approach supports transparent and consistent updates across the codebase
without manually changing values across multiple files.
'''

# === Simulation Control ===
num_agents = 1500 # total number of nodes in the network
seed_count = 10  # number of users initially seeded with news
max_rounds = 500 # max rounds if the spread doesn't die out on its own

# === Role Counts (Baseline) ===
percent_influencers = 0.025
percent_skeptical = 0.57
percent_fact_checkers = 0.30
percent_susceptible = 0.10  # percent of total agents who are susceptible
percent_highly_susceptible_range = (0.05, 0.10)  # percent of susceptible users who are highly susceptible
percent_super_spreader = 0.001  # percent of susceptible users who are super spreaders

# === News Sharing Probabilities (Fake News) ===
p_fake_fact_checker = (0.05, 0.07) # probability of sharing fake news by a fact-checker
p_fake_susceptible = (0.20, 0.30)
p_fake_highly_susceptible = (0.50, 0.70)
p_fake_super_spreader = (0.70, 1.0)
p_fake_normal = (0.11, 0.16) # probability of sharing fake news by an agent who is neither susceptible not skeptical

# === News Sharing Probabilities (Factual News) ===
p_real_normal = (0.06, 0.09)

# === Fact-checking Intervention ===
p_fact_check = 0.3  # probability a fact-checker flags a fake news

p_belief_revision = 0.75 # probability a fact-checker will change their belief on receiving a conflicting news

# === Share Delay Settings ===
fake_delay_distribution = {
    1: 0.85,
    2: 0.10,
    3: 0.05
}
real_delay_distribution = {
    6: 0.85,
    12: 0.10,
    18: 0.05
}

#variants for hypothesis 2
variant_config = {
    'variant_A': False,  # Influencer-controlled seeding
    'variant_B': False,  # Influencer delay boost
    'variant_C': False   # Influencer trust boost
}

# === Network Structure Parameters ===
num_communities = 5
rewire_fraction = 0.1  # the probability of rewiring each edge in Watts-Strogatz model
ba_attachment = 3  # number of edges, each new node attachs to in Barabasi-Albert model
k_neighbors = 10 # each node is joined with its k nearest neighbors in Watts-Strogatz model