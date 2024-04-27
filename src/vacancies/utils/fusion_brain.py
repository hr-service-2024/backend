import json
import time
from base64 import b64decode
import requests

from src.config import settings


class FusionBrain:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }
        self.model = self.get_model()

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, name, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": 'Место, где работает ' + name.lower()
            }
        }

        data = {
            'model_id': (None, self.model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def save_image(self, request_id, attempts=10, delay=5):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                image_data = b64decode(data['images'][0])
                file_path = 'static/img/image.png'
                with open(file_path, 'wb') as file:
                    file.write(image_data)
                return file_path

            attempts -= 1
            time.sleep(delay)


def generate_image(name: str) -> str:
    try:
        api = FusionBrain('https://api-key.fusionbrain.ai/', settings.fusion_brain.FUSION_BRAIN_API_KEY,
                          settings.fusion_brain.FUSION_BRAIN_SECRET_KEY)
        uuid = api.generate(name)
        file_path = api.save_image(uuid)
    except Exception as _ex:
        return 'static/img/reserve.jpg'
    else:
        return file_path
