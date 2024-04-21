# https://oauth.vk.com/authorize?client_id=51848610&redirect_uri=https://api.vk.com/blank.html&scope=photos,wall,offline&response_type=token
import requests


class VkBot:
    def __init__(self, token: str, vk_version: str = '5.131'):
        self.token = token
        self.version = vk_version

    def post_channel(self, data: dict) -> None:
        requests.post(
            url='https://api.vk.com/method/wall.post',
            params={
                'access_token': self.token,
                'v': self.version,
                'message': data.get('text'),
                'owner_id': data.get('vk_channel_id'),
                'attachments': 'photo-224298848_456239018',  # TODO: подгружать фотографию
                'from_group': 1
            }
        )
