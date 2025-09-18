import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RemoteHtmlManager:
    """
    Manages fetching HTML content from remote URLs.
    """

    def fetch_html(self, url: str) -> str:
        """
        Fetches the content of a remote HTML page and returns it as a string.
        SSL verification is disabled for local testing.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The HTML content as a string.
        """
        response = requests.get(url, verify=False)
        response.raise_for_status()
        return response.text
