from apify_client import ApifyClient
import os

# Initialize the ApifyClient with your API token
client = ApifyClient(os.getenv("APIFY_API_KEY"))

# Prepare the Actor input

def get_facebook_events(search_queries, start_urls, max_events):
    run_input = {
        "searchQueries": search_queries,
        "startUrls": start_urls,
        "maxEvents": max_events,
    }
    run = client.actor("UZBnerCFBo5FgGouO").call(run_input=run_input)
    results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        print(item)
        results.append(item)
    return results


#run = get_facebook_events(["louisville festivalls"], [], 10)
#print(run)

