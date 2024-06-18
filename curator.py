from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, ValidationError
from typing import Literal
from generate_images import generate_image
from fireworks_config import logfire, create_gemini_client
from search import search

Curator = APIRouter()

class Activity(BaseModel):
    title: str = Field(..., description="Title of the activity")
    description: str = Field(..., description="Detailed description of what the activity involves")
    activity_type: Literal['restaurant', 'going for drinks', 'physical activity', 'games', 'event'] = Field(..., description="Type of the activity")
    location: str = Field(..., description="Geographical location or venue of the activity")
    result_url: str = Field(..., description="URL of the search result")

class Experience(BaseModel):
    id: str = Field(..., description="Unique identifier for the experience")
    title: str = Field(..., description="Descriptive title of the experience")
    description: str = Field(..., description="Comprehensive description of what the experience entails")
    image_url: str = Field(..., description="URL of the image of the experience")
    image_prompt: str = Field(..., description="Description for generating a representative image of the experience")
    activities: List[Activity] = Field(..., description="List of activities included in the experience. Add more for a faster-paced experience")
    pace: Literal["fast-paced", "slow", "medium"] = Field(..., description="Indicates whether the experience is laid-back or rushed")
    keywords: List[str] = Field(..., description="Keywords that best describe the experience")
    song_of_the_experience: str = Field(..., description="A song that encapsulates the mood or theme of the experience")

client = create_gemini_client("models/gemini-1.5-flash-latest")

@Curator.post("/curation", response_model=List[Experience])
def create_experience(query: str) -> List[Experience]:
    try:
        search_results = search(query)
        if not search_results:
            return []

        user_message = "\n\n".join([
            f"Result Title: {res.ResultTitle}\nResult Text: {res.ResultText}\nResult URL: {res.ResultURL}\nResult ID: {res.ResultID}\nQuery Text: {res.QueryText}" 
            for res in search_results
        ])
        print(user_message)

        # Step 4: Feed the search results to the language model
        experiences: List[Experience] = client.chat.completions.create(
            response_model=List[Experience],
            messages=[
                {
                    "role": "system",
                    "content": """
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










          """,
                },
                {
                    "role": "user",
                    "content": user_message
                },
            ],
        )
        
       # Ensure the raw_experiences data matches the expected structure of Experience
        for experience in experiences:
            answer,file_url = generate_image(experience.image_prompt, f"{experience.id}_image.jpg")
            experience.image_url = file_url  # Ensure this is a string path or URL
        
        return experiences

    except ValidationError as ve:
        print(f"Validation error: {ve}")
        raise HTTPException(status_code=422, detail=ve.errors())
    #except Exception as e:
        #print(f"An error occurred: {e}")
        #raise HTTPException(status_code=500, detail="An unexpected error occurred")
