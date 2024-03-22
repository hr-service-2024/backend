from PIL import Image, ImageDraw, ImageFont
from typing import List
import os
import re

import openai
from base64 import b64decode
from datetime import datetime
# import google.generativeai as genai

from src.config import OPENAI_KEY

openai.api_key = OPENAI_KEY


def fix_mistakes(text: str) -> str:
    content = 'Исправь орфографические ошибки в тексте, не меняя его содержание\n' + text
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': content}]
    )
    response = completion.choices[0].message.content
    return response


def generate_image_chat(name: str) -> str:
    try:
        # raise ValueError
        prompt = 'Сгенерируй фотографию места, где работает ' + name
        response = openai.Image.create(
            prompt=prompt, n=1, size='1024x1024', response_format='b64_json'
        )
        image_data = b64decode(response['data'][0]['b64_json'])
        file_name = datetime.utcnow().strftime('%d-%m-%y_%H-%M') + '.png'
        file_path = os.path.join('static\\img', file_name)
        with open(file_path, 'wb') as file:
            file.write(image_data)
    except Exception as _ex:
        return 'static/img/reserve.jpg'
    else:
        return file_path


def text_to_image(photo_path: str, name: str, responsibilities: List[str]) -> str:
    img = Image.open(photo_path)
    img_draw = ImageDraw.Draw(img)
    font_bold = ImageFont.truetype('static/fonts/Pragmatica-Bold.otf', 26)
    font_regular = ImageFont.truetype('static/fonts/Pragmatica-Regular.otf', 22)

    if photo_path == 'static/img/template1.png':
        name = [line.strip() for line in re.findall(r'.{1,22}(?:\s+|$)', name)]
        img_draw.text((322, 290 - 5 * len(name)), text='\n'.join(name), fill=(0, 0, 0), font=font_bold)

        count_lines = 0
        count_symbols = 0
        for responsibility in responsibilities:
            count_symbols += len(responsibility)
            if count_symbols <= 210:
                responsibility = [line.strip() for line in re.findall(r'.{1,28}(?:\s+|$)', responsibility)]
                img_draw.text((322, 430 + 30 * count_lines), text='\n'.join(responsibility) + '.', fill=(0, 0, 0), font=font_regular)
                count_lines = len(responsibility)
    elif photo_path == 'static/img/template2.png':
        name = [line.strip() for line in re.findall(r'.{1,22}(?:\s+|$)', name)]
        if len(max(name, key=lambda x: len(x))) > 15:
            img_draw.text((350, 210 - 5 * len(name)), text='\n'.join(name), fill=(0, 0, 0), font=font_bold)
        else:
            img_draw.text((425, 210 - 5 * len(name)), text='\n'.join(name), fill=(0, 0, 0), font=font_bold)

        count_lines = 0
        count_symbols = 0
        for responsibility in responsibilities:
            count_symbols += len(responsibility)
            if count_symbols <= 210:
                responsibility = [line.strip() for line in re.findall(r'.{1,28}(?:\s+|$)', responsibility)]
                img_draw.text((42, 300 + 30 * count_lines), text='\n'.join(responsibility) + '.', fill=(0, 0, 0), font=font_regular)
                count_lines += len(responsibility)

    file_path = f"static/img/{photo_path[photo_path.rfind('/') + 1:photo_path.rfind('.')]}_text.png"
    img.save(file_path)
    return file_path


def image_to_image(template_path: str, chat_image_path: str) -> str:
    template_img = Image.open(template_path).convert("RGBA")
    chat_img = Image.open(chat_image_path).convert("RGBA")
    if 'template1' in template_path:
        chat_img = chat_img.crop((chat_img.width // 4, 0, chat_img.width * 3 // 4, chat_img.height))
        template_img.paste(
            chat_img.resize((chat_img.width, chat_img.height)),
            (-chat_img.width // 2, 0),
            chat_img.resize((chat_img.width, chat_img.height))
        )
        draw = ImageDraw.Draw(template_img)
        # закругление
        draw.polygon(((0, 0), (0.5 * chat_img.width, 0), (0.5 * chat_img.width, 0.5 * template_img.height),
                      (0.48 * chat_img.width, 0.45 * template_img.height),
                      (0, 0.02 * template_img.height)), fill=(255, 255, 255))
        draw.polygon(((0, template_img.height), (0.5 * chat_img.width, template_img.height),
                      (0.5 * chat_img.width, 0.5 * template_img.height),
                      (0.48 * chat_img.width, 0.55 * template_img.height),
                      (0, 0.98 * template_img.height)), fill=(255, 255, 255))
    elif 'template2' in template_path:
        chat_img = chat_img.crop((template_img.width // 4, 0.05 * chat_img.height, chat_img.width, chat_img.height))
        template_img.paste(
            chat_img.resize((chat_img.width, chat_img.height)),
            (template_img.width // 4, template_img.height * 2 // 3),
            chat_img.resize((chat_img.width, chat_img.height))
        )
        draw = ImageDraw.Draw(template_img)
        # закругление
        draw.polygon(((template_img.width // 4, template_img.height * 2 // 3), (0.75 * template_img.width, template_img.height * 2 // 3),
                      (0.73 * template_img.width, 0.67 * template_img.height), (template_img.width // 4, template_img.height)),
                     fill=(255, 255, 255))
        draw.polygon(((template_img.width, 0.8 * template_img.height), (template_img.width, template_img.height * 2 // 3),
                      (0.75 * template_img.width, template_img.height * 2 // 3), (0.78 * template_img.width, 0.67 * template_img.height)),
                     fill=(255, 255, 255))

    file_path = 'static/img/result.png'
    template_img.save(file_path)

    if 'reserve.jpg' not in chat_image_path:
        os.remove(chat_image_path)
    os.remove(template_path)

    return file_path


if __name__ == '__main__':
    image_to_image(template_path='static/img/template2_text.png', chat_image_path='static/img/reserve.jpg')
