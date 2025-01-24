from typing import List
from brave import Brave
import json
import os
from pydantic import BaseModel, Field

class SearchResults(BaseModel):
    ResultText: str
    ResultURL: str
    ResultTitle: str
    ResultID: str
    QueryText: str

def search(query: str, num_results: int) -> List[SearchResults]:
    brave = Brave(api_key=os.getenv("BRAVE_API_KEY"))
    search_results = brave.search(q=query, raw=True, num_results=num_results)
    result_objects = []

    for result in search_results:
        search_result = SearchResults(
            ResultText=result['text'],  # Assuming 'text' is the key for the result text
            ResultURL=result['url'],  # Assuming 'url' is the key for the result URL
            ResultTitle=result['title'],  # Assuming 'title' is the key for the result title
            ResultID=result['id'],  # Assuming 'id' is the key for the result ID
            QueryText=query  # The original query text
        )
        result_objects.append(search_result)

    return result_objects



#"""  result = search("""

# Original Query
# I want to plan a day in louisville kentucky like im at the beach

# Question 1:

# What specific aspects of a beach day do you want to replicate in Louisville, such as 
# relaxation, outdoor activities, or seafood?'

# All of the above and just getting in water

# Answer 1:

# Question 2:
# Are there any particular beach-inspired amenities or services you're looking for, like a 
# pool or a beach-themed restaurant?", 


# Answer 2

# beach-themed
# Question3:

# How important is it for you to have a 'beachy' atmosphere, and would you be open to 
# creative alternatives, such as a rooftop or a lakefront, if a traditional beach isn't possible?

# Answer 2
# Its imperative that i have beachy atomsphere, I would be open to alternatives

# Extracted Details:
# (Ambiance=['relaxed', 'beachy'], Mood=['fun', 'carefree'], Vibe=['summer', 'coastal'],
# Pace=['leisurely'],
# ActivityTypes=['swimming', 'outdoor activities', 'water sports'],
# Keywords=['beach-themed', 'pool', 'lakefront', 'rooftop', 'waterfront']



# """ 
#                )

#print(json_data)
# dict_data = [json.loads(item) for item in json_data]
# Pass the list of dictionaries to create_documents
# docs = splitter.create_documents(texts=dict_data)

# for doc in docs[:10]:
#     print(doc)
# dict_data = [json.loads(item) for item in json_data]
# Pass the list of dictionaries to create_documents
# docs = splitter.create_documents(texts=dict_data)

# for doc in docs[:10]:
#     print(doc) """