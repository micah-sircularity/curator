from gather import get_search_results, EventSearch, FacebookSearch, HashtagSearch, GoogleSearch, TiktokSearch, YelpSearch
from functions.events import get_events
from functions.facebook_events import get_facebook_events
from functions.ig_post_finder import fetch_instagram_posts_by_hashtag
from functions.searching import search
from functions.tiktok import search_tiktok_videos
from functions.places import search_yelp_business

def run_match(item):
    """
    Executes the appropriate function based on the type of search result and returns the joined results.

    Parameters:
    item: The search result item whose type will be matched to determine the appropriate function to call.
    """
    result = ""
    match item:
        case EventSearch():
            result = get_events(item.keyword, item.date, item.location)
        case FacebookSearch():
            result = get_facebook_events(item.keyword)
        case HashtagSearch():
            result = fetch_instagram_posts_by_hashtag(item.keyword)
        case GoogleSearch():
            result = search(item.keyword)
        case TiktokSearch():
            result = search_tiktok_videos(item.keyword, item.location)
        case YelpSearch():
            result = search_yelp_business(item.keyword, item.location)
        case _:
            print("Unknown search type")
            result = "Unknown search type"
    
    print(f"Result for item {item}: {result}")
    
    if isinstance(result, list):
        return "\n".join(str(res) for res in result)
    return str(result)




