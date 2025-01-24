from gather import get_search_results, EventSearch, HashtagSearch, GoogleSearch, TiktokSearch, YelpSearch
from functions.events import get_events
#from functions.facebook_events import get_facebook_events
from functions.ig_post_finder import fetch_instagram_posts_by_hashtag
from functions.searching import search
from functions.tiktok import search_tiktok_videos
from functions.places import search_brave_business


def run_match(item):
    """
    Executes the appropriate function based on the type of search result and returns the joined results.

    Parameters:
    item: The search result item whose type will be matched to determine the appropriate function to call.
    """
    result = ""
    match item:
        case EventSearch():
            result = get_events(item.event_search, item.date.name, item.location)
        #case FacebookSearch():
        #    result = get_facebook_events(item.facebook_event_search)
        case HashtagSearch():
            result = fetch_instagram_posts_by_hashtag(item.instagram_search)
        case GoogleSearch():
            result = search(item.google_search)
        case TiktokSearch():
            result = search_tiktok_videos(item.tiktok_search, item.tiktok_location)
        case YelpSearch():
            result = search_brave_business(item.yelp_search, item.yelp_location)
        case _:
            print("Unknown search type")
            result = "Unknown search type"
    
    print(f"Result for item {item}: {result}")
    
    if isinstance(result, list):
        return "\n".join(str(res) for res in result)
    return str(result)





def run_search(search_results):
    results = [run_match(result) for result in search_results]
    return results


 

#test_search = get_search_results("I want to plan a day in Louisville, Kentucky like I'm at the beach")

#new = run_search(test_search)

#print(new)