'''
config.py
Centralizing constants and parameters for
simple tweaking of simulation setup as needed.
'''

# === Simulation Control ===
num_agents = 1500
seed_count = 10  # number of users initially seeded with news
max_rounds = 500

# === Role Counts (Baseline) ===
percent_influencers = 0.025
percent_fact_checkers = 0.39
percent_susceptible = 0.10

# === News Sharing Probabilities (Fake News) ===
p_fake_fact_checker = (0.03, 0.07)
p_fake_susceptible = (0.18, 0.26)
p_fake_normal = (0.15, 0.23)

# === News Sharing Probabilities (Factual News) ===
p_real_normal = (0.06, 0.09)

# === Fact-checking Intervention ===
p_fact_check = 0.3  # probability a fact-checker flags fake news, figure out justification for this - pending

# === Share Delay Settings ===
fake_delay = (1, 2)  # quick reshare
real_delay = (6, 12)  # slower diffusion

# === Network Structure Parameters ===
num_communities = 5  # used in stochastic block model
rewire_fraction = 0.1  # The probability of rewiring each edge in Watts-Strogatz model
ba_attachment = 3  # number of edges, each new node attachs to in Barabasi-Albert model
k_neighbors = 10 #Each node is joined with its k nearest neighbors in Watts-Strogatz model