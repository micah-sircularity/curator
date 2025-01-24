from apify_client import ApifyClient
import os

# Initialize the ApifyClient with your API token
client = ApifyClient(os.getenv("APIFY_API_KEY"))

# Prepare the Actor input

def get_facebook_events(search_queries):
    if not isinstance(search_queries, list):
        search_queries = [search_queries]
    run_input = {
        "searchQueries": search_queries,
        "maxEvents": 10,
    }
    run = client.actor("UZBnerCFBo5FgGouO").call(run_input=run_input)
    results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        print(item)
        results.append(item)
    return results

#run = get_facebook_events(["louisville festivalls"])
#print(run)

