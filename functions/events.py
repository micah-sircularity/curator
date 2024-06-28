import http.client
import os
import pprint
from urllib.parse import quote  # Import the quote function


def get_events(query, date, location):
    conn = http.client.HTTPSConnection("real-time-events-search.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': os.getenv("RAPIDAPI_KEY"),
        'x-rapidapi-host': "real-time-events-search.p.rapidapi.com"
    }

    # Encode the URL components
    query = quote(f"{query} in {location}")
    date = quote(date.encode('utf-8'))  # Ensure date is encoded to bytes before quoting
    # Construct the URL with encoded components
    conn.request("GET", f"/search-events?query={query}&date={date}&is_virtual=false&start=0", headers=headers)
    res = conn.getresponse()
    data = res.read()

    response = (data.decode("utf-8"))
    return response

#run = get_events("festivals", "weekend", "louisville")
#pprint.pprint(run)
