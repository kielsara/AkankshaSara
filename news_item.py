class NewsItem:
    def __init__(self, title, is_fake):
        self.title = title
        self.is_fake = is_fake
        self.shared_count = 0
        self.is_flagged_fake = False


