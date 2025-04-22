import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # load from .env file

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Aizen that can perform various tasks like Alexa and Google Assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ],
    max_tokens=100
)

print(response.choices[0].message.content)
