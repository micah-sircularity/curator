import http.client
import urllib.parse
import json

def search_yelp_business(query, location):
    conn = http.client.HTTPSConnection("yelp-business-api.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "d771574539msh89c78b90d608024p1389a6jsnea6481c12bc0",
        'x-rapidapi-host': "yelp-business-api.p.rapidapi.com"
    }

    encoded_query = urllib.parse.quote_plus(query)
    encoded_location = urllib.parse.quote_plus(location)
    conn.request("GET", f"/search?query={encoded_query}&location={encoded_location}&page=1", headers=headers)

    res = conn.getresponse()
    data = res.read()
    results = json.loads(data.decode("utf-8"))
    
    # Sort results by rating from highest to lowest
    sorted_results = sorted(results['SearchResults'], key=lambda x: x['rating'], reverse=True)
    
    return sorted_results

# Example usage:
#print(search_yelp_business("Fancy Restaurants", "Louisville"))
#