from typing import List

from pydantic import BaseModel, Field

from fireworks_config import client, logfire, openai_client

# Apply the patch to the OpenAI client
# enables response_model keyword

logfire.configure(pydantic_plugin=logfire.PydanticPlugin(record="all"))
logfire.instrument_openai(openai_client)


class QueryGeneration(BaseModel):
  QueryList: List[str] = Field(
      ...,
      description=
      """You are an expert experience curator.

Your goal is to generate relevant queries based on the user's location and context. These queries should help the user uncover and find unique places or activities in their area.

Understand the user's location and context. Tailor all queries to this information.
Generate 10 search engine queries. Each query should be phrased as an answer to help the search engine find the best information for the user.
Ensure all queries are specific and detailed, relevant to the user's location and context.
Example Queries:

"Events this weekend in [User's Location]"
"What are the top-rated hidden gems to visit in [User's Location]?"
"Unique outdoor activities to try in [User's Location] this weekend."
"Best local food experiences in [User's Location] that aren't tourist traps."
"Lesser-known historical sites to explore in [User's Location]."
"What are the must-visit art galleries and museums in [User's Location]?"
"Off-the-beaten-path hiking trails in [User's Location]."
"Upcoming local events and festivals in [User's Location] for [specific month]."
"Top-rated local shops and boutiques to visit in [User's Location]."
"Family-friendly activities to enjoy in [User's Location]."
"Best places to experience the local culture and traditions in [User's Location]."
Ensure that each query is relevant to the user's location and context provided.
"""
  )


@logfire.instrument("query_generation", extract_args=True)
def query_generation(content: str) -> QueryGeneration:
  queries: QueryGeneration = client.chat.completions.create(
      model="accounts/fireworks/models/llama-v3-70b-instruct",
      response_model=QueryGeneration,
      temperature=0.5,
      messages=[
          {
              "role":
              "system",
              "content":
              """Objective:
As an expert curator of experiences, restaurants, and events, your task is to transform
user queries 
into precise, Google-like search queries. 
These queries will
be used to search 
the internet and retrieve the most relevant information to fulfill user requests 
effectively.

Context:
You will be provided with a transcript of a conversation between the user and an agent. 
Your 
role involves analyzing this conversation 
to
identify key 
requirements and preferences expressed by the user.

Guidelines for Query Formation:

Focus on Specificity: Each query should be as specific as possible to the user's interests and the context provided.
Coverage of Key Areas: Ensure that the queries cover the following areas, as relevant:
Activities
Restaurants or Bars
Events
Query Format: Frame your queries in a manner that is optimized for search engines, using
appropriate keywords and phrases that are likely to yield the most relevant results.
Quantity: Generate a total of 10 search engine queries 
structure the queries to look more like answers.

Examples of Good Queries:

"Here are Italian restaurants near Central Park open after 8 PM:"
"Here are Upcoming jazz concerts in Chicago this weekend:"
"These are Top-rated adventure activities for families in Colorado Springs:"
Deliverables:
Submit the list of 10 Google-like queries based on the user-agent conversation context.
Ensure 
each query is distinct and tailored to different aspects of the user's preferences and 
requirements.
 """,
          },
          {
              "role": "user",
              "content": content,
          },
      ],
  )
  return queries


# result = query_generation("""
#   Original Query:
#   I want to plan a day in louisville kentucky like im at the beach
#
#   AgentQuestion 1:
#   What specific aspects of a beach day do you want to replicate in Louisville, such as relaxation, outdoor activities, or seafood?'
#    
#    UserAnswer 1:
#   All of the above and just getting in water
#
#
#   AgentQuestion 2:
#   Are there any particular beach-inspired amenities or services you're 
#   looking for, like a pool or a beach-themed restaurant?", 
#
#
#   UserAnswer 2 beach-themed
#
#   AgentQuestion3:
# How important is it for you to have a 'beachy' atmosphere, and would you be open to 
# creative alternatives, such as a rooftop or a lakefront, if a traditional beach isn't possible?
#
#   UserAnswer 3
#   Its imperative that i have beachy atomsphere, I would be open to alternatives
#
#   Extracted Details:
#   (Ambiance=['relaxed', 'beachy'], Mood=['fun', 'carefree'], Vibe=['summer', 'coastal'],
#   Pace=['leisurely'],
#   ActivityTypes=['swimming', 'outdoor activities', 'water sports'],
#   Keywords=['beach-themed', 'pool', 'lakefront', 'rooftop', 'waterfront']
#
#
#
# """)
# print(result.model_dump_json)
