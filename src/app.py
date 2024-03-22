from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

from src.service import get_vacancy, send_vacancy_to_networks, generate_image

app = FastAPI(title='Service', version='0.0.1')
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/get_vacancy')  # Электрогазосварщик на ВГОК 4, Токарь, Машинист погрузочно-доставочной машины 1
async def show_vacancy(request: Request, vacancy_name: str = Form(...)):
    try:
        vacancy = await get_vacancy(vacancy_name)
    except Exception as _ex:
        return templates.TemplateResponse('index.html', {'request': request, 'error': 'not found'})
    else:
        return templates.TemplateResponse('index.html', {'request': request, 'text': vacancy.text, 'photo_path': vacancy.photo_path, 'vacancy_name': vacancy.name})


@app.post('/regeneration_image')
async def regeneration_image(request: Request, text: str = Form(...), photo_path: str = Form(...), vacancy_name: str = Form(...)):
    photo_path = await generate_image(text.replace('\r', ''), vacancy_name)
    return templates.TemplateResponse('index.html', {'request': request, 'text': text, 'photo_path': photo_path, 'vacancy_name': vacancy_name})


@app.post('/send_vacancy')
async def send_vacancy(request: Request, text: str = Form(...), photo_path: str = Form(...), vacancy_name: str = Form(...), vk: bool = Form(False), tg: bool = Form(False)):
    try:
        if not vk and not tg:
            raise ValueError
        await send_vacancy_to_networks(text, photo_path, vk, tg)
    except Exception as _ex:
        return templates.TemplateResponse('index.html', {'request': request, 'text': text, 'photo_path': photo_path, 'vacancy_name': vacancy_name, 'error': 'error send'})
    else:
        return templates.TemplateResponse('index.html', {'request': request, 'msg': 'success send'})


if __name__ == '__main__':
    uvicorn.run(app)
