'''
simulation.py

This module contains the core simulation logic for modeling the spread of fake and real news
through a synthetic social network. It includes functions for:
- Initializing agents with probabilistic sharing behavior
- Seeding news items into the network (standard or influencer-biased)
- Scheduling shares with delay distributions
- Simulating propagation rounds with belief updates and fact-checker interventions

The simulation supports experimental variants aligned with specific hypotheses:
- Hypothesis 2: Influencer-controlled dynamics (Variants A, B, C)
- Hypothesis 3: Belief revision under competing news exposure

Output metrics include infection counts, belief conversions, and influencer impact.
'''

import random
from collections import defaultdict, deque
from typing import Dict, Tuple, List, Any, Set
import numpy as np
import networkx as nx
from config import *
from news_item import NewsItem
from agent_initializer import Agent


def initialize_p_shares(agents: Dict[int, Agent]) -> None:
    """
    Assigns probabilistic share likelihoods to each agent based on their role.

    Parameters:
        agents : dict. Dictionary mapping agent ID to Agent instance.

    Returns:
        None

    Examples:
        >>> from agent_initializer import Agent
        >>> agents = {0: Agent(0)}
        >>> initialize_p_shares(agents)
        >>> isinstance(agents[0].p_share_fake, float)
        True
        >>> 0.0 <= agents[0].p_share_fake <= 1.0
        True
        >>> 0.0 <= agents[0].p_share_real <= 1.0
        True
    """
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


def select_initial_seeds(agents: Dict[int, Agent], news_type: str) -> List[int]:
    """
    Randomly selects a set of seed agents and assigns them a belief state.

    Parameters:
        agents : dict. All agents in the simulation.
        news_type : str. Either 'fake' or 'real'.

    Returns:
        List: list. List of agent IDs seeded with the news.
    """
    seeds = random.sample(list(agents.keys()), seed_count)
    for uid in seeds:
        agents[uid].belief_state = news_type
    return seeds


def select_initial_seeds_variant(agents: Dict[int, Agent], news_type: str) -> List[int]:
    """
    Selects seed users for news introduction with preference for influencers (Variant A).

    Parameters:
        agents : dict. Mapping of agent IDs to Agent objects.
        news_type : str. Either 'fake' or 'real'.

    Returns:
        List : list. List of seeded agent IDs.
    """
    influencers = [uid for uid, agent in agents.items() if agent.is_influencer]
    others = [uid for uid in agents if uid not in influencers]
    seed_influencers = random.sample(influencers, min(7, len(influencers)))
    seed_others = random.sample(others, seed_count - len(seed_influencers))
    seeds = seed_influencers + seed_others
    for uid in seeds:
        agents[uid].belief_state = news_type
    return seeds


def sample_delay_from_distribution(delay_dist: Dict[int, float], agent: Agent, news_type: str, variant_flag_dict: Dict[str, bool] = variant_config) -> int:
    """
    Samples a delay (in rounds) from a distribution based on user role and variant flags.

    Parameters:
        delay_dist : dict. Delay distribution dictionary (delay: probability).
        agent : Agent. The agent sharing the news.
        news_type : str. Either 'fake' or 'real'.
        variant_flag_dict : dict. Configuration flags for enabled variants.

    Returns:
        int : int. The number of rounds to delay.
    Examples:
        >>> import random; random.seed(0)
        >>> from agent_initializer import Agent
        >>> agent = Agent(2)
        >>> delay_dist = {1: 0.7, 2: 0.3}
        >>> sample_delay_from_distribution(delay_dist, agent, 'real', {'variant_B': False}) in delay_dist
        True
    """
    if news_type == 'fake' and variant_flag_dict['variant_B'] and agent.is_influencer:
        delay_dist = {1: 0.95, 2: 0.05}
    rand_val = random.random()
    cumulative = 0.0
    for delay, prob in sorted(delay_dist.items()):
        cumulative += prob
        if rand_val <= cumulative:
            return delay
    return max(delay_dist.keys())


def schedule_initial_shares(seeds: List[int], agents: Dict[int, Agent], news_type: str, schedule: Dict[int, List[Tuple[int, str]]], delay_offset: int = 0, variant_flag_dict: Dict[str, bool] = variant_config) -> None:
    """
    Adds initial share events to the schedule queue for each seeded user.

    Parameters:
        seeds : list. List of seeded agent IDs.
        agents : dict. Mapping of agent ID to Agent.
        news_type : str. Either 'fake' or 'real'.
        schedule : dict. A schedule of future events (round: list of (user, news_type)).
        delay_offset : int. Additional delay offset for real news (used in Hypothesis 3).
        variant_flag_dict : dict. Variant control flags.

    Returns:
        None
    """
    dist = fake_delay_distribution if news_type == 'fake' else real_delay_distribution
    for uid in seeds:
        delay = sample_delay_from_distribution(dist, agents[uid], news_type,variant_flag_dict=variant_flag_dict)
        schedule[delay + delay_offset].append((uid, news_type))


def modified_trust(source_agent: Agent, trust: float, variant_flag_dict: Dict[str, bool] = variant_config) -> float:
    """
    Applies a trust multiplier if the source is an influencer (Variant C).

    Parameters:
        source_agent : Agent. The agent sharing the news.
        trust : float. Original trust value.
        variant_flag_dict : dict. Flags for controlling variant logic.

    Returns:
        float : float. Modified trust value.
    Examples:
        >>> from agent_initializer import Agent
        >>> agent = Agent(1)
        >>> agent.is_influencer = True
        >>> modified_trust(agent, 0.5, {'variant_C': True})
        0.6
        >>> modified_trust(agent, 0.5, {'variant_C': False})
        0.5
    """
    return trust * 1.2 if variant_flag_dict['variant_C'] and source_agent.is_influencer else trust

def simulate_spread(G: nx.Graph, agents: Dict[int, Agent], news_items: Dict[str, NewsItem], hypothesis=None, real_news_delay=0,
                    variant_flag_dict: Dict[str, Any] = variant_config,) -> tuple[dict[str, list[Any]], dict[str, int], int | Any, dict[str, int] | None]:
    """
    Simulates the round-based spread of fake and real news through a social network.
    Agents may adopt beliefs, share news with delays, and revise beliefs based on trust,
    role, and external fact-checker intervention. Includes support for:
    - Hypothesis 2: Influencer-controlled variants (A, B, C)
    - Hypothesis 3: Competing real vs. fake news with belief revision

    Parameters:
    G : nx.Graph. The social network graph with trust-weighted edges.
    agents : dict. Mapping of agent IDs to Agent objects.
    news_items : dict. Dictionary with 'fake' and 'real' NewsItem instances.
    hypothesis : str or None. One of 'h2', 'h3', or None to control variant logic.
    real_news_delay : int. Optional delay in seeding real news (used in Hypothesis 3).
    variant_flag_dict : dict. Dictionary of variant activation flags.

    Returns:
        stats : dict[str, list[int]]. Infection count by round for each news type.
        final_beliefs : dict[str, int]. Final number of agents believing fake or real news.
        belief_revised_count : int. Number of agents who switched beliefs after receiving conflicting news.
        influencer_impact : dict[str, int]. Spread attribution (influencer vs. normal) for fake news (only in H2).

    Examples:
        >>> import networkx as nx
        >>> G = nx.erdos_renyi_graph(50, 0.1)
        >>> from agent_initializer import assign_roles
        >>> from news_item import NewsItem
        >>> agents = assign_roles(G)
        >>> initialize_p_shares(agents)
        >>> news_items = {'fake': NewsItem("Fake", is_fake=True), 'real': NewsItem("Real", is_fake=False)}
        >>> simulate_spread(G, agents, news_items)  # doctest: +SKIP
    """
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
                continue # this agent has already shared this news type, so continue

            # Agent shares the news now
            agent.has_shared[news_type] = True
            news_items[news_type].shared_count += 1

            # Propagate to neighbors
            for neighbor_id in G.neighbors(uid):
                neighbor = agents[neighbor_id]

                if neighbor.belief_state is not None: # This neighbor already believes a news type

                    # Check for hypothesis 3
                    if hypothesis == 'h3' and neighbor.belief_state != news_type:
                        # if this agent already believes in a news but received a conflicting news
                        # they may check the fact and change their belief state
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
                    trust *= 0.3 # reduce trust for flagged fake news

                prob = agent.p_share_fake if news_type == 'fake' else agent.p_share_real
                if random.random() < prob * trust:  # if the effective probability falls within a random theshold, then share the news
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

        stats['fake'].append(len(infected['fake'])) # how many agents got infected with the fake news in current round
        stats['real'].append(len(infected['real'])) # how many agents got infected with the real news in current round
        if not schedule: # spread is over
            break

    influencer_impact = {'influencer': 0, 'normal': 0}
    # track how many users got infected with the fake news when source of information was an influencer
    if hypothesis == 'h2':
        influencer_impact = {
            'influencer': sum(1 for uid in infected['fake'] if source_map.get(uid) == 'influencer'),
            'normal': sum(1 for uid in infected['fake'] if source_map.get(uid) == 'normal')
        }
    final_beliefs = {'fake': 0, 'real': 0} # final belief count for each type of news at the end of each simulation
    for agent in agents.values():
        if agent.belief_state == 'fake':
            final_beliefs['fake'] += 1
        elif agent.belief_state == 'real':
            final_beliefs['real'] += 1


    return stats, final_beliefs, belief_revised_count, influencer_impact