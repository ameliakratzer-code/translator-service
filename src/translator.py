import os
from dotenv import load_dotenv
import openai
import ast

# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = openai.OpenAI(
    api_key=openai_api_key
)

def query_llm_robust(post: str) -> tuple[bool, str]:
  context = "First, determine the language of the given post. If the post is written in English, return True and the original post. Next, if the post is not in English, return False and the English translation. If the post is unintelligible (e.g., contains random characters or gibberish), return False and the original post. Desired format: A tuple where (True if the post is in English and False if not, translated post or original post)."
  response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {
            "role": "system",
            "content": context
          },
          {
              "role": "user",
              "content": post
          }
      ]
    )
  response = response.choices[0].message.content
  try:
    response = response.strip("'")  # Remove outer single quotes if present
    parsed = ast.literal_eval(response)
    if isinstance(parsed, tuple) and len(parsed) == 2 and isinstance(parsed[0], bool) and isinstance(parsed[1], str):
      return parsed
    else:
      return (False, "__LLM_ERROR__: " + post)
  except (SyntaxError, ValueError, TypeError):
    pass  # Handle cases where parsing fails
  return (False, "__LLM_ERROR__: " + post)