import os
import shutil

import openai
from dotenv import load_dotenv

load_dotenv()

terminal_width = shutil.get_terminal_size().columns

openai.api_key = os.getenv('API_KEY')

dialog_message = 'Enter your prompt. (Please enter "exit()" to terminate)\n\n'
context = ''

while True:
    prompt = input(dialog_message)
    if prompt == 'exit()':
        break

    context += f"user:{prompt}\n"

    print('\nGenerating response...\n')
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": context}],
            temperature=0.0,
        )
        answer = response["choices"][0]["message"]["content"]
        context += f'assistant:{answer}\n'
    except openai.error.APIError as e:
        answer = e.error
        break

    print(answer.replace('assistant:', ''))
    print('-' * terminal_width, '\n' * 2)
