import requests

class NitrousOxiClient:
    def __init__(self, base_url="https://api.nitrous-oxi.de"):
        self.base_url = base_url

    def fetch_data(self, category, query):
        url = f"{self.base_url}/{category}?query={query}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return data.get("data", {})
            except ValueError:
                raise ValueError(f"Invalid JSON response for {query} in {category}")
        elif response.status_code == 404:
            raise ValueError(f"No data found for {query} in {category}")
        else:
            raise ValueError(f"Error fetching data for {query} in {category}")
