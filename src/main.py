import json
from bs4 import BeautifulSoup

from src.telegram.tg_bot import TelegramBot
from config import TG_TOKEN, TG_CHANNEL_ID, VK_CHANNEL_ID, PHOTO_PATH


def main(vacancy_name: str):
    data = {
        'tg_channel_id': TG_CHANNEL_ID,
        'vk_channel_id': VK_CHANNEL_ID,
        'photo_path': PHOTO_PATH,
        'text': ''
    }

    with open('../storage/Вакансии.json', encoding='UTF-8') as file:
        vacancies = json.loads(file.read())
    for v in vacancies['items']:
        if v['status'] == 1 and v['name'] == vacancy_name and any(dct.get('value', 0) == 76 for dct in v['customFieldsValues']):
            data['text'] = BeautifulSoup(v['description'], 'html.parser').text.strip()

    TelegramBot(token=TG_TOKEN).post_channel(data)


if __name__ == '__main__':
    vacancy = input('Введите название профессии: ')  # Электрогазосварщик на ВГОК 4
    main(vacancy)
