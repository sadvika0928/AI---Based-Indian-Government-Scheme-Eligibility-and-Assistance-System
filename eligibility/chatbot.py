import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("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")  # or hardcode your key temporarily

def ask_chatbot(question):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or gpt-3.5-turbo for cheaper
        messages=[
            {"role": "system", "content": "You are a helpful assistant who guides users about Indian government schemes."},
            {"role": "user", "content": question}
        ],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']
