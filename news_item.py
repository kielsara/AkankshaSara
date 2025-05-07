class NewsItem:
    def __init__(self, title, is_fake, related_id=None, is_related=False):
        self.title = title
        self.is_fake = is_fake
        self.shared_count = 0
        self.is_flagged_fake = False