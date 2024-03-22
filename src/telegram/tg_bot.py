import telebot


class TelegramBot:
    def __init__(self, token: str, parse_mode: str = 'HTML'):
        self.bot = telebot.TeleBot(token=token, parse_mode=parse_mode)

    def post_channel(self, data: dict) -> None:
        photo = open(data.get('photo_path'), 'rb')
        text = data.get('text')
        if len(text) > 1000:
            for i in range(len(text)//1000 + 1):
                if i < len(text)//1000:
                    line_length = text[:1000].rfind('\n')
                    paragraph = text[:line_length + 1]
                    text = text[line_length + 1:]
                else:
                    paragraph = text
                if i == 0:
                    self.bot.send_photo(data.get('tg_channel_id'), photo=photo, caption=paragraph)
                else:
                    self.bot.send_message(data.get('tg_channel_id'), text=paragraph)
        else:
            self.bot.send_photo(data.get('tg_channel_id'), photo=photo, caption=text)
