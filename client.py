from openai import OpenAI

client = OpenAI(
)

completion = client.chat.completions.create(
  model = "gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "you are a virtual assistance named Jarvis skilled in general tasks like amazon and google cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)