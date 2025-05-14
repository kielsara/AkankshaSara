import random
from collections import defaultdict, deque
from typing import Dict, Tuple, List, Any, Set

import numpy as np
import networkx as nx

from config import *
from news_item import NewsItem
from agent_initializer import Agent


def initialize_p_shares(agents: Dict[int, Agent]):
    for agent in agents.values():
        try:
            if agent.is_fact_checker:
                agent.p_share_fake = np.random.uniform(*p_fake_fact_checker)
            elif agent.is_susceptible:
                if agent.susceptible_type == "super_spreader":
                    agent.p_share_fake = np.random.uniform(*p_fake_super_spreader)
                elif agent.susceptible_type == "highly_susceptible":
                    agent.p_share_fake = np.random.uniform(*p_fake_highly_susceptible)
                else:
                    agent.p_share_fake = np.random.uniform(*p_fake_susceptible)
            else:
                agent.p_share_fake = np.random.uniform(*p_fake_normal)
            agent.p_share_real = np.random.uniform(*p_real_normal)
        except Exception as e:
            print(f"Error initializing p_shares for agent {agent.id}: {e}")


def select_initial_seeds(agents, news_type):
    seeds = random.sample(list(agents.keys()), seed_count)
    for uid in seeds:
        agents[uid].belief_state = news_type
    return seeds

# --- Override seeding to include influencer control (Variant A) ---
def select_initial_seeds_variant(agents, news_type):
    influencers = [uid for uid, agent in agents.items() if agent.is_influencer]
    others = [uid for uid in agents if uid not in influencers]
    seed_influencers = random.sample(influencers, min(7, len(influencers)))
    seed_others = random.sample(others, seed_count - len(seed_influencers))
    seeds = seed_influencers + seed_others
    for uid in seeds:
        agents[uid].belief_state = news_type
    return seeds

def sample_delay_from_distribution(delay_dist: Dict[int, float], agent, news_type,variant_flag_dict=variant_config) -> int:

    # Delay sampling with influencer override (Variant B)
    if news_type == 'fake' and variant_flag_dict['variant_B'] and agent.is_influencer:
        delay_dist = {1: 0.95, 2: 0.05}
    rand_val = random.random()
    cumulative = 0.0
    for delay, prob in sorted(delay_dist.items()):
        cumulative += prob
        if rand_val <= cumulative:
            return delay
    return max(delay_dist.keys()) # fallback


def schedule_initial_shares(seeds, agents, news_type, schedule, delay_offset=0,variant_flag_dict=variant_config) -> int:
    dist = fake_delay_distribution if news_type == 'fake' else real_delay_distribution
    for uid in seeds:
        delay = sample_delay_from_distribution(dist, agents[uid], news_type,variant_flag_dict=variant_flag_dict)
        schedule[delay + delay_offset].append((uid, news_type))

# --- Trust boost if influencer is the source (Variant C) ---
def modified_trust(source_agent, trust,variant_flag_dict=variant_config,):
    return trust * 1.2 if variant_flag_dict['variant_C'] and source_agent.is_influencer else trust

def simulate_spread(
    G: nx.Graph,
    agents: Dict[int, Agent],
    news_items: Dict[str, NewsItem],
    hypothesis=None,
    real_news_delay=0,
    variant_flag_dict: Dict[str, Any] = variant_config,
) -> tuple[dict[str, list[Any]], dict[str, int], int | Any, dict[str, int] | None]:
    schedule = defaultdict(list) #e.g - { 7 :[ ( 1239, "real") ], 2 : [( 1100, "fake")]} Will first get updated with initial seed numbers and then later with neighbors
    stats = {'fake': [], 'real': []}
    infected = {'fake': set(), 'real': set()}
    belief_revised_count = 0
    source_map = {}  # uid -> 'influencer' or 'normal'

    for news_type in ['fake', 'real']:  # Initialize seeds for both news types
        delay_round = real_news_delay if news_type == 'real' and hypothesis == 'h3' else 0 #for hypothesis 3, add a delay for real news
        if hypothesis == 'h2' and variant_flag_dict['variant_A']:
            seeds = select_initial_seeds_variant(agents, news_type)
            # Track origin type for seeds
            for uid in seeds:
                source_map[uid] = 'influencer' if agents[uid].is_influencer else 'normal'
        else:
            seeds = select_initial_seeds(agents, news_type)

        schedule_initial_shares(seeds, agents, news_type, schedule, delay_round, variant_flag_dict=variant_flag_dict)
        infected[news_type].update(seeds)

    # Run simulation rounds
    for round_num in range(max_rounds): #500
        current_events = schedule.pop(round_num, [])
        random.shuffle(current_events) # Randomize processing order of events to avoid bias

        for uid, news_type in current_events:
            agent = agents[uid]
            if agent.has_shared[news_type]:
                continue #this agent has already shared this news type, so continue

            # Agent shares the news now
            agent.has_shared[news_type] = True
            #shared[news_type].add(uid)
            news_items[news_type].shared_count += 1

            # Propagate to neighbors
            for neighbor_id in G.neighbors(uid):
                neighbor = agents[neighbor_id]

                if neighbor.belief_state is not None: # This neighbor already believes a news type

                    #Check for hypothesis 3
                    if hypothesis == 'h3' and neighbor.belief_state != news_type:
                        #if this agent already believes in a news but received a conflicting news
                        #they may check the fact and change their belief state
                        revision_chance = p_belief_revision if neighbor.is_fact_checker else 0.25
                        if random.random() < revision_chance:
                            neighbor.belief_state = news_type
                            infected[news_type].add(neighbor_id)
                            belief_revised_count += 1
                            delay = sample_delay_from_distribution(
                                real_delay_distribution if news_type == 'real' else fake_delay_distribution,
                                neighbor, news_type
                            )
                            schedule[round_num + delay].append((neighbor_id, news_type))
                    continue # since this agent already believes a news type, continue to the next neighbor

                # change the belief state of the neighbor, if he doesn't believe any news type yet
                trust = G[uid][neighbor_id].get('trust', 0.5)
                trust = modified_trust(agent, trust, variant_flag_dict=variant_flag_dict)
                if news_type == 'fake' and news_items['fake'].is_flagged_fake:
                    trust *= 0.3 # Reduce trust for flagged fake news

                prob = agent.p_share_fake if news_type == 'fake' else agent.p_share_real
                if random.random() < prob * trust:  #if the effective probability falls within a random theshold, then share the news
                    # Fact-checker intervention
                    if news_type == 'fake' and neighbor.is_fact_checker:
                        if random.random() < p_fact_check:
                            news_items['fake'].is_flagged_fake = True

                    # Commit to believe the current news if this neighbor doesn't believe any news yet
                    neighbor.belief_state = news_type
                    infected[news_type].add(neighbor_id)
                    if hypothesis == 'h2' and variant_flag_dict['variant_A']:
                        source_map[neighbor_id] = source_map.get(uid, 'unknown')  # Inherit source for comparison during H2
                    delay = sample_delay_from_distribution(
                        fake_delay_distribution if news_type == 'fake' else real_delay_distribution,
                        neighbor, news_type, variant_flag_dict=variant_flag_dict
                    )
                    schedule[round_num + delay].append((neighbor_id, news_type))

        stats['fake'].append(len(infected['fake'])) #how many agents got infected with the fake news in current run
        stats['real'].append(len(infected['real'])) #how many agents got infected with the real news in current run
        if not schedule: #spread is over
            break

    influencer_impact = {'influencer': 0, 'normal': 0}
    if hypothesis == 'h2':
        influencer_impact = {
            'influencer': sum(1 for uid in infected['fake'] if source_map.get(uid) == 'influencer'),
            'normal': sum(1 for uid in infected['fake'] if source_map.get(uid) == 'normal')
        }
    final_beliefs = {'fake': 0, 'real': 0} #final belief count for each type of news at the end of each simulation
    for agent in agents.values():
        if agent.belief_state == 'fake':
            final_beliefs['fake'] += 1
        elif agent.belief_state == 'real':
            final_beliefs['real'] += 1


    return stats, final_beliefs, belief_revised_count, influencer_impact


