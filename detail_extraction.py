from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field

from fireworks_config import client, logfire, openai_client

# Apply the patch to the OpenAI client
# enables response_model keyword
detail_router = APIRouter()

logfire.configure(pydantic_plugin=logfire.PydanticPlugin(record="all")) 
logfire.instrument_openai(openai_client)

class DetailExtraction(BaseModel):
  Ambiance : List[str] = Field(..., description="Predicted Ambiance of the user query")
  Mood : List[str] = Field(..., description="Predicted Mood of the user query")
  Vibe : List[str] = Field(..., description="Predicted Vibe of the user query")
  Pace : List[str] = Field(..., description="Predicted Pace of the user query")
  ActivityTypes : List[str] = Field(..., description="""Recommended activity types 
  basing on the user query""")
  Keywords: List[str] = Field(..., description="""Recommended keywords based on the user
query
""")

@logfire.instrument("detail_extraction", extract_args=True)
@detail_router.post("/detail_extraction", response_model=DetailExtraction)
def detail_extraction(content: str) -> DetailExtraction:
    details: DetailExtraction = client.chat.completions.create(
        model="accounts/fireworks/models/llama-v3-70b-instruct",
        response_model=DetailExtraction,
        temperature=0.5,
        messages=[
            {
                "role":
                "system",
                "content":
                """As an expert curator of experiences, restaurants, and events, your role 
                is to deeply understand user queries and ensure precise fulfillment of their 
                requests. To achieve this, you must ask targeted clarifying questions. 

Your goal is to extract the expected ambiance,vibe, or tone the user is looking for.
 """,
            },
            {
                "role": "user",
                "content": content,
            },
        ],
    )
    return details

# details = detail_extraction("I want to plan a day in louisville kentucky like im at the beach")
