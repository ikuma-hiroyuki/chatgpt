import os
import shutil

import openai
from dotenv import load_dotenv
from colorama import Fore, Style

load_dotenv()

terminal_width = shutil.get_terminal_size().columns

openai.api_key = os.getenv('API_KEY')

dialog_message = Fore.GREEN + 'Enter your prompt. (Please enter "exit()" to terminate)\n\n' + Style.RESET_ALL
context = ''

while True:
    prompt = input(dialog_message)
    if prompt == 'exit()':
        break

    context += f"user:{prompt}\n"

    print(Fore.CYAN + '\nGenerating response...\n' + Style.RESET_ALL)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": context}],
            temperature=0.0,
        )
        answer = response["choices"][0]["message"]["content"]
        context += f'assistant:{answer}\n'
    except openai.error.APIError as e:
        print(e)
    else:
        print(answer.replace('assistant:', ''))

    print('-' * terminal_width)
