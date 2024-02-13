from dotenv import load_dotenv
import os

load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHANNEL_ID = int(os.getenv('TG_CHANNEL_ID'))
VK_CHANNEL_ID = int(os.getenv('VK_CHANNEL_ID'))
PHOTO_PATH = '../storage/images/Электрогазосварщик.jpg'  # позже будем под профессию подбирать фотографию, сейчас пока что заготовленная
