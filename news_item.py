'''
newsitem.py

This module defines the NewsItem class, which represents a single piece of news
(either fake or real) circulating through the simulated social network.

Each NewsItem tracks:
- Its title and whether it is classified as fake.
- Whether it has been flagged by a fact-checker.
- How many times it has been shared across the network.

This object is passed into the simulation engine and used to model
diffusion dynamics, flagging behavior, and competitive spread (real vs. fake news).
It is used extensively in belief updates, trust modeling, and tracking news propagation.
'''

class NewsItem:
    """
    Represents a piece of news, either fake or real, being propagated through the network.

    Attributes:
        title : str. A human-readable label or headline for the news item.
        is_fake : bool. Indicates whether the news item is classified as misinformation (True) or factual (False).
        shared_count : int. Tracks how many agents have shared this news item during simulation.
        is_flagged_fake : bool. Whether this item has been flagged as fake by a fact-checker in the network.
    """
    def __init__(self, title, is_fake):
        self.title = title
        self.is_fake = is_fake
        self.shared_count = 0
        self.is_flagged_fake = False