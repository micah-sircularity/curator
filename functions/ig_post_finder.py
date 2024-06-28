import http.client

def fetch_instagram_posts_by_hashtag(hashtag):
    conn = http.client.HTTPSConnection("instagram-scraper-api2.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "d771574539msh89c78b90d608024p1389a6jsnea6481c12bc0",
        'x-rapidapi-host': "instagram-scraper-api2.p.rapidapi.com"
    }
    conn.request("GET", f"/v1/hashtag?hashtag={hashtag}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

# Example usage:
#result = fetch_instagram_posts_by_hashtag("louisvilleeats")
#print(result)
