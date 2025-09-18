from finance import FinanceData, Interval
from utils import jump_detected

# Set up interval for 2025-08-01 with 1h interval
interval = Interval(start_date="2025-08-01", end_date="2025-08-02", interval="1h")

# Set time zone to Berlin (Europe/Berlin, GMT+2)
time_zone = "Europe/Berlin"

# Create FinanceData instance
finance_data = FinanceData(ticker="BMW.DE", interval=interval, time_zone=time_zone)

# Fetch data
finance_data.fetch()

# Convert to Berlin time zone
finance_data.convert_timezone()

# Example: Get and print all OHLC values for a given date and hour
date_str = "2025-08-01"
hour_str = "11:53"
ohlc = finance_data.get_hour_value(date_str, hour_str)

if ohlc:
    print(f"OHLC values for {date_str} {hour_str}:")
    for k, v in ohlc.items():
        print(f"  {k}: {v}")
    # Detect jump between Open and High (example: 5% jump)
    jump_percent = 0.5
    if jump_detected(ohlc['Open'], ohlc['High'], jump_percent):
        print(f"Jump detected between Open and High (>{jump_percent}%): True")
    else:
        print(f"Jump detected between Open and High (>{jump_percent}%): False")
else:
    print(f"No data found for {date_str} {hour_str}")

# Optionally, print hourly prices by day
# finance_data.print_hourly_prices_by_day()
# Optionally, print hourly prices by day
# finance_data.print_hourly_prices_by_day()
