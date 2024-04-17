from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # take environment variables from .env.
client = OpenAI()

# Create and execute message request
# https://platform.openai.com/docs/guides/text-generation
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)