import openai

from src.config import OPENAI_KEY

openai.api_key = OPENAI_KEY


def fix_mistakes(text: str) -> str:
    content = 'Исправь орфографические ошибки в тексте, не меняя его содержание\n' + text
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': content}]
    )
    response = completion.choices[0].message.content
    return response
