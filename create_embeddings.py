import openai
import os


client = openai.OpenAI(
  base_url = "https://api.fireworks.ai/inference/v1",
  api_key = os.getenv("FIREWORKS_API_KEY"),
)

def create_embeddings(text: str) -> str:
  response = client.embeddings.create(
  model="nomic-ai/nomic-embed-text-v1.5",
  input=text,
)
  return response.data[0].embedding