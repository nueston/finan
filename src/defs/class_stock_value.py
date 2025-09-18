class Ohlc:
    def __init__(self, m_open: float, m_high: float, m_low: float, m_close: float):
        self.m_open = m_open
        self.m_high = m_high
        self.m_low = m_low
        self.m_close = m_close

    def __repr__(self):
        return (
            f"StockValue(Open={self.m_open}, High={self.m_high}, "
            f"Low={self.m_low}, Close={self.m_close})"
        )
