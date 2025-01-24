import http.client
import urllib.parse
import pprint
import json

def search_tiktok_videos(keyword, location):
    conn = http.client.HTTPSConnection("tiktok-scraper7.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "d771574539msh89c78b90d608024p1389a6jsnea6481c12bc0",
        'x-rapidapi-host': "tiktok-scraper7.p.rapidapi.com"
    }
    # Encode keyword and location to ensure URL compatibility
    encoded_keyword = urllib.parse.quote_plus(f"{keyword} in {location}")
    conn.request("GET", f"/feed/search?keywords={encoded_keyword}&region=us&count=10&cursor=0&publish_time=0&sort_type=0", headers=headers)
    res = conn.getresponse()
    data = res.read()
    results = data.decode("utf-8")

    # Parse the JSON response
    results_json = json.loads(results)
    videos = results_json['data']['videos']
    parsed_videos = [{'title': video['title'], 'video_url': video['play']} for video in videos]
    return parsed_videos

#run = search_tiktok_videos("fancy restaurants in louisville kentucky", "us")
#pprint.pprint(run)