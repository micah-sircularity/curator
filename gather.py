from __future__ import annotations
import instructor
import openai
from typing import Iterable, List, Union
from pydantic import BaseModel, Field
from enum import Enum


class DateOptions(Enum):
        ANY = 'any'
        TODAY = 'today'
        TOMORROW = 'tomorrow'
        WEEK = 'week'
        WEEKEND = 'weekend'
        NEXT_WEEK = 'next_week'
        MONTH = 'month'
        NEXT_MONTH = 'next_month'


class EventSearch(BaseModel):
    keyword: str
    location: str
    date: DateOptions


class FacebookSearch(BaseModel):
    keyword: str
    max_results: int = 20


class HashtagSearch(BaseModel):
    hashtag: str = Field(..., description="The hashtag to search for")


class FindRelevantHashtags:
     query: str = Field(..., description="The hashtag to search for")


class GoogleSearch(BaseModel):
    keyword: str = Field(..., description="The google search query to search for")

class TiktokSearch(BaseModel):
    keyword: str = Field(..., description="The tiktok search query to search for")
    location: str = Field(default="us", description="The location to search for")

class YelpSearch(BaseModel):
    keyword: str = Field(..., description="The yelp search query to search for")
    location: str = Field(..., description="The location to search for")


client = instructor.from_openai(
    openai.OpenAI(), mode=instructor.Mode.PARALLEL_TOOLS
)  


def get_search_results(prompt: str):    
    response = client.chat.completions.create(
        model="gpt-4o",
    messages=[
        {"role": "system", "content": """
        You are an expert experience curator.
  You have a list of search results from a search query. 
  Create 5 unique experiences based on these results,
    each consisting of at least 3 different activities, with a maximum of 5 activities per experience
    Choose from the following activity types (do not repeat any activity type within a single experience):

Restaurant
Going for drinks
Physical activity
Games
Event
Example of how you might structure your selections:

Experience 1:

Event
Games
Restaurant
Experience 2:

Restaurant
Drinks
Event
Experience 3:

Physical activity
Event
Restaurant
Experience 4:

Games
Physical activity
Drinks
Experience 5:

Restaurant
Physical activity
Event
Ensure that each experience is unique and contains 
a mix of the provided activity types without repeating any 
activity type within a single experience.
         
Here is a brief description of the tools:
EventSearch: Search for events in a specific location for a specific keyword, this should be used for finding relevant events
FacebookSearch: Search for Facebook posts for a specific keyword, this should be used for finding relevant events in the area
HashtagSearch: Search for hashtags on social media, this should be used for finding info from bloggers or influencers
GoogleSearch: Search for Google results for a specific keyword, this should be used for general purpose context
TiktokSearch: Search for Tiktok results for a specific keyword, this should be used when you want to uncover more unique results
YelpSearch: Search for Yelp results for a specific keyword, this should be used when you want to find placesHer
         
You should always use more than one tool, and you should always use tiktok, google, and yelp.

         """},
        {"role": "user", "content": prompt}
    ],
    response_model = Iterable[EventSearch | FacebookSearch | HashtagSearch | GoogleSearch | TiktokSearch | YelpSearch]
)
    return response


#results = (get_search_results("I want to plan a day in Louisville, Kentucky like I'm at the beach"))

#for result in results:
    #print(f"Tool: {type(result).__name__}, Result: {result}")
