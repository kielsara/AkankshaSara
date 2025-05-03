'''
config.py
Centralizing constants and parameters for
simple tweaking of simulation setup as needed.
'''

# === Simulation Control ===
num_agents = 1500
num_seeds = 1  # number of users initially seeded with news
num_simulation_rounds = 20
num_trials = 1000

# === Role Counts (Baseline) ===
influencer_fraction = 0.025
fact_checker_fraction = 0.57
susceptible_fraction = 0.10

# remove these? - pending
# num_influencers = int(num_agents * influencer_fraction)
# num_fact_checkers = int(num_agents * fact_checker_fraction)
# num_susceptible_users = int(num_agents * susceptible_fraction)
# num_regular_users = num_agents - (num_influencers + num_fact_checkers + num_susceptible_users)

# === News Sharing Probabilities (Fake News)
p_share_fake_fact_checker_range = (0.03, 0.07)
p_share_fake_susceptible_range = (0.17, 0.22)
p_share_fake_normal_range = (0.11, 0.16)

# === News Sharing Probabilities (Factual News)
p_share_real_normal_range = (0.065, 0.094)

# === Fact-checking Intervention ===
p_fact_check = 0.5  # probability a fact-checker flags fake news

# === Trust Levels by Edge Type ===
trust_within_direct = (0.8, 1.0)
trust_within_indirect = (0.5, 0.7)
trust_between_communities = (0.1, 0.4)
trust_threshold = 0.6  # below this, agents don’t believe/share what they receive

# === Share Delay Settings ===
share_delay_fake_range = (1, 2)  # quick reshare
share_delay_real_range = (6, 12)  # slower diffusion

# === Network Structure Parameters ===
num_communities = 5  # used in stochastic block model
rewire_fraction = 0.2  # The probability of rewiring each edge in Watts-Strogatz model
ba_attachment = 3  # number of edges, each new node attachs to in Barabasi-Albert model
k_neighbors = 10 #Each node is joined with its k nearest neighbors in Watts-Strogatz model