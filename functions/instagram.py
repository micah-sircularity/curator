import http.client
import urllib.parse
import json

def search_instagram_hashtags(search_query):
    conn = http.client.HTTPSConnection("instagram-scraper-api2.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "d771574539msh89c78b90d608024p1389a6jsnea6481c12bc0",
        'x-rapidapi-host': "instagram-scraper-api2.p.rapidapi.com"
    }
    # Encode the search query to ensure URL compatibility
    encoded_query = urllib.parse.quote_plus(search_query)
    conn.request("GET", f"/v1/search_hashtags?search_query={encoded_query}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    data_decoded = data.decode("utf-8")
    
    # Parse the JSON response
    data_json = json.loads(data_decoded)
    
    # Find the hashtag with the highest media count
    max_media_count = -1
    top_hashtag = None
    for hashtag in data_json['data']['items']:
        if hashtag['media_count'] > max_media_count:
            max_media_count = hashtag['media_count']
            top_hashtag = hashtag['name']
    return top_hashtag

#run = search_instagram_hashtags("thingstodoinlouisville")
#print(run)
