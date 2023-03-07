import os

import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('API_KEY')

dialog_message = 'Enter your prompt. (Please enter "exit()" to terminate)\n'
context = ''

while True:
    prompt = f"Q:{input(dialog_message)}\n"
    if prompt == 'Q:exit()\n':
        break

    context += prompt

    if prompt:
        print('\nGenerating response...\n')
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": context}],
            temperature=0.0,
        )

        answer = f'A:{response["choices"][0]["message"]["content"]}'
        context += answer
        print(f'{answer}', '\n' * 5)
