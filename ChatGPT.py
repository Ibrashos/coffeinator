import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("TOKEN_GPT")


def chat(text: str, token: str = openai.api_key):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{text}",
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0)
    return response['choices'][0]['text']

