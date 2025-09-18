class NewsEntry:
    def __init__(self, date: str, time: str, company: str, sentiment: int, impact: int):
        self.date = date
        self.time = time
        self.company = company
        self.sentiment = sentiment
        self.impact = impact

    def __repr__(self):
        return f"[{self.date}, {self.time}, {self.company}, {self.sentiment}, {self.impact}]"
