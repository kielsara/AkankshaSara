'''
config.py
Centralizing constants and parameters for
simple tweaking of simulation setup as needed.
'''

# === Simulation Control ===
num_agents = 1500
num_communities = 5
nodes_per_community = num_agents // num_communities
num_influencers = 5
num_fact_checkers = 100
num_susceptible_users = 100
num_normal_users = num_agents - (num_susceptible_users+num_influencers+num_fact_checkers)

num_seeds = 3  # number of users initially seeded with news

num_simulation_rounds = 15
num_mc_runs = 100

# === News Spread Probabilities ===
'''everything below this needs updated still!!!'''
p_share_fake = 0.2
p_share_real = 0.1

p_share_fake_influencer = 0.3
p_share_fake_skeptic = 0.05
p_share_fake_factchecker = 0.0

p_share_real_influencer = 0.15
p_share_real_susceptible = 0.07
p_share_real_factchecker = 0.1
p_share_real_normal = 0.1

p_fact_check = 0.5  # chance a fact-checker flags false info

# === Trust Parameters (Edge Weights) ===
trust_within_community = (0.5, 1.0)
trust_between_communities = (0.2, 0.7)

# === News Spread Delay (in time steps) ===
share_delay_fake = (1, 2)  # use random.randint(*share_delay_fake)
share_delay_real = (2, 6)