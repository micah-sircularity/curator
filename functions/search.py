from typing import List
import json

from exa_py import Exa
from pydantic import BaseModel, Field
from langchain_text_splitters import RecursiveJsonSplitter


from query_generations import query_generation

# Initialize the Exa client with the API key
exa = Exa(api_key="13368f79-5f89-487e-b860-3c94cdeaa0ae")

class ExtractedDetails(BaseModel):
    Entities: str = Field(..., description="Entities")
    chunks: str = Field(..., description="separate the text chunks by relevance")


class SearchResults(BaseModel):
    ResultText: str
    ResultURL: str
    ResultTitle: str
    ResultID: str
    QueryText: str

splitter = RecursiveJsonSplitter(max_chunk_size=2000)

    

def search(query: str) -> List[SearchResults]:
    query_list = query_generation(query)
    result_objects = []

    for item in query_list.QueryList:
        search_response = exa.search_and_contents(item,use_autoprompt=True,
        type="magic", num_results=5)
        for result in search_response.results:
            # Accessing properties directly
            search_result = SearchResults(
                ResultText=result.text,  # Adjusted to use the highlights property
                ResultURL=result.url,
                ResultTitle=result.title,
                ResultID=result.id,
                QueryText=item
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