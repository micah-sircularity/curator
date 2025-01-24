import os

import instructor
import logfire
from openai import OpenAI
import google.generativeai as genai


openai_client = OpenAI()
#logfire.configure(pydantic_plugin=logfire.PydanticPlugin(record="all")) 
#logfire.instrument_openai(openai_client)


def create_client():
    base_url = "https://api.fireworks.ai/inference/v1"
    api_key = os.getenv("FIREWORKS_API_KEY")
    if not api_key:
        raise ValueError("FIREWORKS_API_KEY is not set in the environment variables.")

    client = instructor.patch(
        OpenAI(
            base_url=base_url,
            api_key=api_key,
        ),
        # Customize further if other modes or configurations are needed
    )
    client = instructor.from_openai(client, mode=instructor.Mode.MD_JSON)
    return client

client = create_client()


def create_gemini_client(model_name: str):
    client = instructor.from_gemini(
        client=genai.GenerativeModel(
            model_name=model_name,  # model defaults to "gemini-pro"
        ),
        mode=instructor.Mode.GEMINI_JSON,
    )
    return client




