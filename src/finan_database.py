import os
import csv
from defs.class_news import NewsEntry
from typing import List

class FinanDatabase:


    def __init__(self, out_dir: str):
        self.out_dir = out_dir
        os.makedirs(self.out_dir, exist_ok=True)

    def get_news_from_csv(self, date: str) -> List[NewsEntry]:
        """
        Load news entries from a CSV file for the given date.

        Args:
            date (str): The date string in 'YYYY-MM-DD' format, used in the filename.

        Returns:
            List[NewsEntry]: List of news entries loaded from the CSV file.
        """
        csv_path = os.path.join(self.out_dir, f'stock_news_{date}.csv')
        entries = []
        if not os.path.exists(csv_path):
            return entries
        with open(csv_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                entry = NewsEntry(
                    date=row['date'],
                    time=row['time'],
                    ticker=row['ticker'],
                    sentiment=int(row['sentiment']),
                    impact=int(row['impact'])
                )
                entries.append(entry)
        return entries

    def save_news_to_csv(self, entries: List[NewsEntry], date: str) -> str:
        """
        Save news entries as a CSV file in the output folder.

        Args:
            entries (List[NewsEntry]): List of news entries to save.
            date (str): The date string in 'YYYY-MM-DD' format, used in the filename.

        Returns:
            str: The path to the saved CSV file.
        """
        csv_path = os.path.join(self.out_dir, f'stock_news_{date}.csv')
        with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['date', 'time', 'ticker', 'sentiment', 'impact'])
            for entry in entries:
                writer.writerow([entry.date, entry.time, entry.ticker, entry.sentiment, entry.impact])
        return csv_path
