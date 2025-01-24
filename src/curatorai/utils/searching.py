from typing import List
import json
import os

from exa_py import Exa
from pydantic import BaseModel, Field
from langchain_text_splitters import RecursiveJsonSplitter

# Initialize the Exa client with the API key
exa = Exa(api_key=os.getenv("EXA_API_KEY"))

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
    result_objects = []

    search_response = exa.search_and_contents(query, use_autoprompt=True, type="magic", num_results=5)
    for result in search_response.results:
        # Accessing properties directly
        search_result = SearchResults(
            ResultText=result.text,
            ResultURL=result.url,
            ResultTitle=result.title,
            ResultID=result.id,
            QueryText=query
        )
        result_objects.append(search_result)

    return result_objects


#print(search("I want to plan a day in Louisville, Kentucky like I'm at the beach"))
