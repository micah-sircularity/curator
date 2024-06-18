from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field

from fireworks_config import client, logfire, openai_client

# Apply the patch to the OpenAI client
Clarifyingrouter = APIRouter()

# enables response_model keyword
logfire.configure(pydantic_plugin=logfire.PydanticPlugin(record="all")) 
logfire.instrument_openai(openai_client)

class ClarifyingQA(BaseModel):
    QuestionsAndAnswers: List[dict] = Field(
          ..., description="""Each item is an object with a 
          'question' and 'answers' key, where 'answers' is a list of up to 10 multiselect options excluding 'other'.""")

class QueryUnderstanding(BaseModel):
  clarifying_qa: ClarifyingQA

  Reasoning: List[str] = Field(
      ..., description="List your reasoning for the question you asked")
    

@logfire.instrument("clarifying_questions", extract_args=True)

@Clarifyingrouter.post("/clarifying_questions", response_model=QueryUnderstanding)
def query_understanding(content: str) -> QueryUnderstanding:
    qa: QueryUnderstanding = client.chat.completions.create(
        model="accounts/fireworks/models/llama-v3-70b-instruct",
        response_model=QueryUnderstanding,
        temperature=0.5,
        messages=[
            {
                "role": "system",
                "content": """As an expert curator of experiences, restaurants, and 
                events, 
                your 
objective is to delve deeply into the user's unique interests and expectations. 
To achieve
a precise 
understanding of their desires, you should pose targeted and insightful questions.

Consider these guidelines when crafting your questions:

Users often have idealized visions inspired by media or previous experiences. Aim to
identify 
these influences.
Clarify any metaphors or similes the user employs to ensure alignment with their true 
preferences.
Bridge the gap between their imaginative expectations and realistic possibilities through 
your inquiries.
Provide three questions to the user that will help elucidate their specific needs and 
enhance your ability to curate a personalized experience.

Along with the questions you should include
answers to the questions you asked. Please return 10 potential options for the users to
select from.
Your questions should be at a 5th grade reading level.
""",
            },
            {
                "role": "user",
                "content": content,  # Use the `query` parameter instead of the hardcoded string
            },
        ],
    )
    return qa

###qa = query_understanding("I want to plan a day in louisville kentucky like im at the beach")
###print(qa.model_dump_json)
