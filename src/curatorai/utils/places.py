import requests
import json
import os

def search_brave_business(query, location):
    url = f"https://api.search.brave.com/res/v1/web/search?q={query}+in+{location}"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": os.environ.get("BRAVE_API_KEY")
    }

    response = requests.get(url, headers=headers)
    results = response.json()
    return results

# Example usage:
#print(search_brave_business("Greek Restaurants", "San Francisco"))
