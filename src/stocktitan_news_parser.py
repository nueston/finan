
import re
from bs4 import BeautifulSoup
from typing import List, Dict
from remote_html_manager import RemoteHtmlManager
from defs.class_news import NewsEntry



class StockNewsParser:

    def __init__(self, url: str, date: str):
        """
        Initialize the parser by fetching HTML content for a specific date from the given base URL.

        Args:
            url (str): The base URL.
            date (str): The date string in 'YYYY-MM-DD' format.
        """
        fetch_url = f"{url}/news/{date}"
        html_content = RemoteHtmlManager().fetch_html(fetch_url)
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def parse_news_entries(self) -> List[NewsEntry]:
        """
        Parse news entries from the HTML content.

        Returns:
            List[NewsEntry]: List of parsed news entries.
        """
        entries = []
        # Find all news entry blocks by 'news-row' class
        for entry in self.soup.find_all('div', class_=re.compile(r'news-row')):
            date = self._extract_date(entry)
            time = self._extract_time(entry)
            ticker = self._extract_ticker(entry)
            sentiment = self._extract_sentiment(entry)
            impact = self._extract_impact(entry)
            if date and time and ticker:
                entries.append(NewsEntry(date, time, ticker, sentiment, impact))
        return entries


    def _extract_date(self, entry) -> str:
        # Example: <span name="date">02.08.2025</span>
        date_tag = entry.find('span', attrs={'name': 'date'})
        return date_tag.text.strip() if date_tag else ''

    def _extract_time(self, entry) -> str:
        time_tag = entry.find('span', attrs={'name': 'time'})
        if time_tag:
            return time_tag.text.strip()
        # fallback: try class 'news-row-date'
        time_tag = entry.find('span', class_=re.compile(r'news-row-date'))
        return time_tag.text.strip() if time_tag else ''

    def _extract_ticker(self, entry) -> str:
        # Find ticker symbol in news-list-tickers
        tickers_div = entry.find('div', attrs={'name': 'tickers'})
        if tickers_div:
            symbol_link = tickers_div.find('a', class_=re.compile(r'symbol-link'))
            if symbol_link:
                return symbol_link.text.strip()
        return ''

    def _extract_sentiment(self, entry) -> int:
        # Find sentiment-bar and count .dot.full
        sentiment_bar = entry.find('div', class_=re.compile(r'sentiment-bar'))
        if sentiment_bar:
            full_dots = len(sentiment_bar.find_all('span', class_=re.compile(r'dot\s*full')))
            return full_dots
        return 0

    def _extract_impact(self, entry) -> int:
        # Find impact-bar and count .dot.full
        impact_bar = entry.find('div', class_=re.compile(r'impact-bar'))
        if impact_bar:
            full_dots = len(impact_bar.find_all('span', class_=re.compile(r'dot\s*full')))
            return full_dots
        return 0

# Example usage

url = 'https://www.stocktitan.net'
date = '2025-08-01'
parser = StockNewsParser(url, date)
news_entries = parser.parse_news_entries()
for entry in news_entries:
    print(entry)
