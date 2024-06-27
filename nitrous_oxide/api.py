import requests
from typing import Union, List, Dict


class NitrousOxiClient:
    def __init__(self, base_url: str = "https://api.nitrous-oxi.de"):
        self.base_url = base_url

    def _make_request(self, url: str) -> Union[List, Dict]:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()

    def fetch_data(self, category: str, query: str) -> Union[List, Dict]:
        url = f"{self.base_url}/{category}?query={query}"
        data = self._make_request(url)

        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data.get("data", {})
        else:
            raise ValueError(f"Unexpected response format for {query} in {category}")


