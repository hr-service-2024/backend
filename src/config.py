from dotenv import load_dotenv
import os

load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHANNEL_ID = int(os.getenv('TG_CHANNEL_ID'))
VK_TOKEN = os.getenv('VK_TOKEN')
VK_CHANNEL_ID = int(os.getenv('VK_CHANNEL_ID'))
OPENAI_KEY = os.getenv('OPENAI_KEY')
