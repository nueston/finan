class NewsEntry:
    def __init__(self, date: str, time: str, ticker: str, sentiment: int, impact: int):
        self.date = date
        self.time = time
        self.ticker = ticker
        self.sentiment = sentiment
        self.impact = impact

    def __repr__(self):
        return f"[{self.date}, {self.time}, {self.ticker}, {self.sentiment}, {self.impact}]"
