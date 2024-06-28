from pydantic import BaseModel
# Adjust the import statement to reference the parent directory
import sys
sys.path.append('../')  # Adds the parent directory to the system path
from fireworks_config import *

class Hashtag(BaseModel):
    hashtag: str


def generate_hashtags(query):
    response = client.chat.completions.create(
        model="accounts/fireworks/models/firefunction-v2",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates hashtags for a given query."},
            {"role": "user", "content": "I want to spend the day in louisville kentucky like im at the beach"}
        ],
        response_model=Hashtag,
        max_retries=3,
        strict=True
    )

    print(response)

    return response


#run = generate_hashtags("I want to spend the day in louisville kentucky like im at the beach")

#print(run)

