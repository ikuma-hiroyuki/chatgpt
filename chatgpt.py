import os
import shutil

import openai
from colorama import Fore
from dotenv import load_dotenv
from rich.console import Console
from rich.syntax import Syntax


def output_terminal(lines):
    print(f'{Fore.GREEN}AI: {Fore.RESET}', end='')
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
    os.system("cls" if os.name == "nt" else "clear")
    print("AIアシスタントとチャットを始めます。チャットを終了させる場合は exit() と入力してください。")
    system_content = input("AIアシスタントに演じてほしい役割がある場合は入力してください。(ない場合はエンターキーを押してください。):\n")

    messages = []
    if system_content:
        messages.append({"role": "system", "content": system_content})

    while True:
        user_input = input(f"{Fore.CYAN}あなた: {Fore.RESET}")
        if user_input == 'exit()':
            break

        print()
        messages.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(model=os.getenv("MODEL"), messages=messages)
        answer = response['choices'][0]['message']
        output_terminal(answer['content'])
        print("-" * terminal_width)

        messages.append({"role": answer['role'], "content": answer['content']})


if __name__ == '__main__':
    # 初期設定
    terminal_width = shutil.get_terminal_size().columns
    console = Console()
    load_dotenv()
    openai.api_key = os.getenv('API_KEY')

    chat()
