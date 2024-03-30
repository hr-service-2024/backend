from PIL import Image, ImageDraw, ImageFont
import re
import os


def text_to_image(photo_path: str, name: str, text: str) -> str:
    img = Image.open(photo_path)
    img_draw = ImageDraw.Draw(img)
    font_bold = ImageFont.truetype('static/fonts/Pragmatica-Bold.otf', 26)
    font_regular = ImageFont.truetype('static/fonts/Pragmatica-Regular.otf', 22)

    txt = text.split('\n')
    list_text = []
    try:
        for fragment in txt[txt.index('Обязанности:') + 1:]:
            if len(list_text) > 0 and fragment == '':
                break
            elif fragment != '':
                list_text.append(fragment)
    except Exception as _ex:
        for fragment in txt[txt.index('Требования:') + 1:]:
            if len(list_text) > 0 and fragment == '':
                break
            elif fragment != '':
                list_text.append(fragment)

    if 'template1' in photo_path:
        name = [line.strip() for line in re.findall(r'.{1,22}(?:\s+|$)', name)]
        img_draw.text((322, 290 - 5 * len(name)), text='\n'.join(name), fill=(0, 0, 0), font=font_bold)

        count_lines = 0
        count_symbols = 0
        for fragment in list_text:
            count_symbols += len(fragment)
            if count_symbols <= 200:
                fragment = [line.strip() for line in re.findall(r'.{1,28}(?:\s+|$)', fragment)]
                img_draw.text((322, 430 + 30 * count_lines), text='\n'.join(fragment) + '.', fill=(0, 0, 0),
                              font=font_regular)
                count_lines = len(fragment)
    elif 'template2' in photo_path:
        name = [line.strip() for line in re.findall(r'.{1,22}(?:\s+|$)', name)]
        if len(max(name, key=lambda x: len(x))) > 15:
            img_draw.text((350, 210 - 5 * len(name)), text='\n'.join(name), fill=(0, 0, 0), font=font_bold)
        else:
            img_draw.text((425, 210 - 5 * len(name)), text='\n'.join(name), fill=(0, 0, 0), font=font_bold)

        count_lines = 0
        count_symbols = 0
        for fragment in list_text:
            count_symbols += len(fragment)
            if count_symbols <= 200:
                fragment = [line.strip() for line in re.findall(r'.{1,28}(?:\s+|$)', fragment)]
                img_draw.text((42, 300 + 30 * count_lines), text='\n'.join(fragment) + '.', fill=(0, 0, 0),
                              font=font_regular)
                count_lines += len(fragment)

    file_path = 'static/img/result.png'
    img.save(file_path)

    os.remove(photo_path)

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
            (template_img.width // 4, round(0.55 * template_img.height)),
            chat_img.resize((chat_img.width, chat_img.height))
        )
        draw = ImageDraw.Draw(template_img)
        # закругление
        draw.polygon(((template_img.width // 4, 0.55 * template_img.height),
                      (0.75 * template_img.width, 0.55 * template_img.height),
                      (0.73 * template_img.width, 0.56 * template_img.height),
                      (template_img.width // 4, template_img.height)),
                     fill=(255, 255, 255))
        draw.polygon(((template_img.width, 0.7 * template_img.height), (template_img.width, 0.55 * template_img.height),
                      (0.78 * template_img.width, 0.55 * template_img.height),
                      (0.8 * template_img.width, 0.56 * template_img.height)),
                     fill=(255, 255, 255))

    file_path = f"static/img/{template_path[template_path.rfind('/') + 1:template_path.rfind('.')]}_image.png"
    template_img.save(file_path)

    if 'reserve.jpg' not in chat_image_path:
        os.remove(chat_image_path)

    return file_path


if __name__ == '__main__':
    image_to_image(template_path='static/img/template2.png', chat_image_path='static/img/reserve.jpg')
