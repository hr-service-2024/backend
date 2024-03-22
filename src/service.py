import json
import os
from bs4 import BeautifulSoup
from random import randint

from src.config import TG_TOKEN, TG_CHANNEL_ID, VK_TOKEN, VK_CHANNEL_ID
from src.schemas import ShowVacancy
from src.telegram.tg_bot import TelegramBot
from src.vkontakte.vk_bot import VkBot
from src.utils import fix_mistakes, text_to_image, generate_image_chat, image_to_image

last_template = None


async def generate_image(text: str, name: str) -> str:
    global last_template
    try:
        txt = text.split('\n\n')
        responsibilities = txt[txt.index('Обязанности:') + 1:][0].split('\n')
        if last_template == 1:
            template_number = 2
        elif last_template == 2:
            template_number = 1
        else:
            template_number = randint(1, 2)
        template_path = f'static/img/template{template_number}.png'
        template_with_text_path = text_to_image(template_path, name, responsibilities)

        chat_image_path = generate_image_chat(name)
        photo_path = image_to_image(template_with_text_path, chat_image_path)
    except Exception as _ex:
        return 'static/img/reserve.jpg'
    else:
        last_template = template_number
        return photo_path


async def get_vacancy(vacancy_name: str) -> ShowVacancy:
    data = dict()

    with open('../storage/Вакансии.json', encoding='UTF-8') as file:  # TODO: вакансии подгружаются из Friend Work
        vacancies = json.loads(file.read())

    for v in vacancies['items']:
        if v['status'] == 1 and v['name'].lower() == vacancy_name.lower() and any(dct.get('value', 0) == 76 for dct in v['customFieldsValues']):
            # text = fix_mistakes(text=BeautifulSoup(v['description'], 'html.parser').text.strip())
            text = BeautifulSoup(v['description'], 'html.parser').text.strip()
            data['text'] = '#Работа_ВолковскийГОК\n\n' + text + '\n\nЗвоните, пишите нам прямо сейчас!\n☎️+79812025274 Мария Войничева'
            break

    data['photo_path'] = await generate_image(text, v['name'])
    data['name'] = v['name']

    vacancy = ShowVacancy(**data)
    return vacancy


async def send_vacancy_to_networks(text: str, photo_path: str, vk: bool, tg: bool) -> None:
    data = {
        'tg_channel_id': TG_CHANNEL_ID,
        'vk_channel_id': VK_CHANNEL_ID,
        'text': text,
        'photo_path': photo_path
    }
    if tg:
        TelegramBot(token=TG_TOKEN).post_channel(data=data)
    if vk:
        VkBot(token=VK_TOKEN).post_channel(data=data)
    os.remove(photo_path)
