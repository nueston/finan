
import yfinance as yf
import pandas as pd
import pytz
from defs.class_stock_value import Ohlc


class Interval:
    """
    Represents a time interval for stock data fetching.
    """

    def __init__(self, start_date: str, end_date: str, interval: str = "1d"):
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval  # e.g., '1h', '1d', etc.


class FinanceData:
    """
    Fetches and processes stock data for a given ticker and interval.
    """

    @staticmethod
    def to_lower_interval(time_str: str, time_half: bool = False) -> str:
        """
        Convert an exact time string to its lower hour or half-hour interval.

        Args:
            time_str (str): Time in 'HH:MM' format.
            time_half (bool): If True, round down to nearest half hour (e.g., 10:13 -> 09:30).
                              If False, round down to nearest hour (e.g., 10:13 -> 10:00).

        Returns:
            str: Rounded time string in 'HH:MM' format.
        """
        hour, minute = map(int, time_str.split(":"))
        if time_half:
            if minute < 30:
                hour = hour - 1 if hour > 0 else 23
                return f"{hour:02d}:30"
            else:
                return f"{hour:02d}:30"
        else:
            return f"{hour:02d}:00"

    def get_hour_value(self, date_str: str, hour_str: str, time_half: bool = False) -> 'Ohlc | None':
        """
        Get all OHLC values (Open, High, Low, Close) for a given date and hour as a StockValue.

        Args:
            date_str (str): Date in 'YYYY-MM-DD' format.
            hour_str (str): Hour in 'HH:MM' format (24h).
            time_half (bool): If True, round down to nearest half hour.

        Returns:
            StockValue or None: StockValue instance with OHLC, or None if not found.
        """
        if self.data is None or self.data.empty:
            return None
        df = self.data.copy()
        df['date'] = df.index.strftime('%Y-%m-%d')
        df['hour'] = df.index.strftime('%H:%M')
        hour_interval = self.to_lower_interval(hour_str, time_half=time_half)
        mask = (df['date'] == date_str) & (df['hour'] == hour_interval)
        # df mask example:
        # datetime                   Open       High       Low        Close           Volume  Dividends      Stock Splits        date        hour
        # 2025-08-01 09:00:00+02:00  83.480003  83.680000  82.699997  83.019997       0        0.0           0.0                 2025-08-01  09:00
        # ...

        row = df[mask]
        if row.empty:
            print("row empty !!")
            return None
        o = float(row['Open'].max())
        h = float(row['High'].max())
        l = float(row['Low'].max())
        c = float(row['Close'].max())
        return Ohlc(m_open=o, m_high=h, m_low=l, m_close=c)

    def __init__(self, ticker: str, interval: Interval, time_zone: str = 'Europe/Berlin'):
        self.ticker = ticker
        self.interval = interval
        self.time_zone = time_zone
        self.data = None

    def convert_timezone(self):
        """
        Convert the DataFrame index to the specified time zone.
        """
        if self.data is not None and not self.data.empty:
            self.data.index = self.data.index.tz_convert(self.time_zone)
        return self.data

    def fetch(self):
        """
        Fetch stock data using yfinance Ticker object.
        """
        ticker_obj = yf.Ticker(self.ticker)
        self.data = ticker_obj.history(
            start=self.interval.start_date,
            end=self.interval.end_date,
            interval=self.interval.interval
        )
        return self.data

    def print_hourly_prices_by_day(self, tz_offset_hours: int = 2):
        """
        Print hourly prices grouped by day, with timezone offset.

        Args:
            tz_offset_hours (int): Timezone offset in hours.
        """
        if self.data is None or self.data.empty:
            print("No data found for the selected range.")
            return
        from datetime import timedelta
        tz_offset = timedelta(hours=tz_offset_hours)
        data_local = self.data.copy()
        data_local.index = data_local.index + tz_offset
        data_local['date'] = data_local.index.strftime('%Y-%m-%d')
        data_local['hour'] = data_local.index.strftime('%H:%M')
        for day, group in data_local.groupby('date'):
            print(f"\n{day}:")
            for _, row in group.iterrows():
                price = row['High']
                if isinstance(price, pd.Series):
                    price = price.iloc[0]
                print(f"  {row['hour']}: {price:.2f}")
