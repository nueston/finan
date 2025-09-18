import yfinance as yf
from datetime import datetime, timedelta


class StockPriceFetcher:
    """
    Fetches stock price from Yahoo Finance for a given ticker, date, and hour.
    """

    def fetch_price(self, ticker: str, date: str, hour: str) -> float:
        """
        Fetches the closing price for the given ticker at the specified date and hour.

        Args:
            ticker (str): The stock ticker symbol.
            date (str): Date in 'DD.MM.YYYY' format.
            hour (str): Hour in 'HH:MM' format.

        Returns:
            float: Price as float, or None if not found.
        """
        dt = datetime.strptime(f"{date} {hour}", "%d.%m.%Y %H:%M")
        start = dt - timedelta(minutes=1)
        end = dt + timedelta(minutes=1)
        df = yf.download(
            ticker,
            start=start.strftime('%Y-%m-%d %H:%M'),
            end=end.strftime('%Y-%m-%d %H:%M'),
            interval='1m'
        )
        if not df.empty:
            closest = df.iloc[0]
            return float(closest['Close'])
        return None
