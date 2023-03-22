import os
import shutil

import openai
from colorama import Fore, Style
from dotenv import load_dotenv
from rich.console import Console
from rich.syntax import Syntax

console = Console()


def output_terminal(lines):
    code_lines = ''
    language = ''
    is_code_block = False
    for line in lines.split('\n'):
        if line.startswith('```'):
            if not is_code_block:
                language = line.replace('```', '')
                is_code_block = True
            else:
                code_syntax = Syntax(code_lines, language, theme="monokai")
                console.print(code_syntax)
                code_lines = ''
                is_code_block = False
        elif is_code_block:
            code_lines += f'{line}\n'
        elif not (code_lines and is_code_block):
            print(line)


def chat():
    load_dotenv()
    openai.api_key = os.getenv('API_KEY')
    terminal_width = shutil.get_terminal_size().columns
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
        except openai.error.APIError as e:
            print(e)
        else:
            context += f'assistant:{answer}\n'
            output_terminal(answer)

        print('-' * terminal_width)


if __name__ == '__main__':
    chat()
