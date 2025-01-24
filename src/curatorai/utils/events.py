import http.client
import os
import pprint
from urllib.parse import quote  # Import the quote function
import json
from brave import Brave



# def get_events(query, date, location):
#     conn = http.client.HTTPSConnection("real-time-events-search.p.rapidapi.com")
#
#     headers = {
#         'x-rapidapi-key': os.getenv("RAPIDAPI_KEY"),
#         'x-rapidapi-host': "real-time-events-search.p.rapidapi.com"
#     }
#
#     # Encode the URL components
#     query = quote(f"{query} in {location}")
#     date = quote(date)  # Encode the date
#     # Construct the URL with encoded components
#     conn.request("GET", f"/search-events?query={query}&date={date}&is_virtual=false&start=0", headers=headers)
#     res = conn.getresponse()
#     data = res.read()
#
#     # Decode the response and parse it as JSON
#     results = data.decode("utf-8")
#
#     # Parse the JSON response
#     results_json = json.loads(results)
#     return results_json
# run = get_events("festivals", "weekend", "louisville")
# pprint.pprint(run)

def get_events(query, date, location):
    brave = Brave()
    num_results = 10
    query = f"{query} in {location} this {date}"
    search_results = brave.search(q=query, raw=True)
    return search_results

#query = "festivals"
#date = "weekend"
#location = "louisville"
#search_results = get_events(query, date, location)
#pprint.pprint(search_results)
