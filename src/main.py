


from finance import FinanceData, Interval
from utils import jump_detected, to_24h
from defs.class_stock_value import Ohlc
from config_manager import ConfigManager
from finan_database import FinanDatabase
import os

def get_news(url, date):
    from stocktitan_news_parser import StockNewsParser

    parser = StockNewsParser(url, date)
    news_entries = parser.parse_news_entries()
    return news_entries

def get_stock_ohlc(ticker: str, start_date_str: str, end_date_str: str, hour_str: str, time_zone: str = "Europe/Berlin") -> Ohlc | None:
    """
    Fetch OHLC data for a given ticker, date, and hour.

    Args:
        ticker (str): Stock ticker symbol.
        date_str (str): Date in 'YYYY-MM-DD' format.
        hour_str (str): Hour in 'HH:MM' format (24h).
        time_zone (str): Time zone string, default is 'Europe/Berlin'.

    Returns:
        Ohlc or None: Ohlc instance with OHLC data, or None if not found.
    """
    # Set up interval for the given date with 1h interval
    interval = Interval(start_date=start_date_str, end_date=end_date_str, interval="1h")

    # Create FinanceData instance (fetch and timezone conversion are automatic)
    finance_data = FinanceData(ticker=ticker, interval=interval, time_zone=time_zone)
    # Get OHLC values
    ohlc = finance_data.get_hour_value(start_date_str, hour_str)
    return ohlc


def main() -> None:
    """
    Main entry point for fetching and displaying finance data.
    """
    config = ConfigManager()
    url = config.url
    time_zone = config.time_zone
    start_date_str = "2025-08-01"
    end_date_str = "2025-08-02"
    hour_str = "11:53"


    news_list = get_news(url, start_date_str)
    # Save news_list to CSV using FinanDatabase
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'out')
    db = FinanDatabase(out_dir)
    db.save_news_to_csv(news_list, start_date_str)
    news_list = db.get_news_from_csv(start_date_str)

    # Example: Get and print all OHLC values for a given date and hour

    for entry in news_list:
        print(to_24h(entry.time))
        interval = Interval(start_date=start_date_str, end_date=end_date_str, interval="1h")
        finance_data = FinanceData(ticker=entry.ticker, interval=interval, time_zone=time_zone)
        ohlc = finance_data.get_hour_value(start_date_str, to_24h(entry.time))
        #print(ohlc.__repr__())


    # Create FinanceData instance for jump detection
    interval = Interval(start_date=start_date_str, end_date=end_date_str, interval="1h")
    finance_data = FinanceData(ticker="BMW.DE", interval=interval, time_zone=time_zone)
    ohlc = finance_data.get_hour_value(start_date_str, hour_str)

    if ohlc:
        print(f"OHLC values for {start_date_str} {hour_str}:")
        print(ohlc.__repr__())
        # Detect jump between Open and High (example: 5% jump)
        jump_percent = 0.5
        if finance_data.isJumpDetected(start_date_str, hour_str, jump_percent):
            print(f"Jump detected between Open and High (>{jump_percent}%): True")
        else:
            print(f"Jump detected between Open and High (>{jump_percent}%): False")
    else:
        print(f"No data found for {start_date_str} {hour_str}")

    # Optionally, print hourly prices by day
    # finance_data.print_hourly_prices_by_day()


if __name__ == "__main__":
    main()
