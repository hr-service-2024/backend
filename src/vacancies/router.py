from fastapi import APIRouter, Depends
from typing import Annotated

from src.auth.utils import get_current_active_user
from src.auth.schemas import UserSchema

router = APIRouter(
    prefix='/vacancies',
    tags=['Vacancies']
)


@router.get('/')
def get_user(user: Annotated[UserSchema, Depends(get_current_active_user)]):
    return user

# @router.get('/')
# async def index(request: Request):
#     return templates.TemplateResponse('index.html', {'request': request})
#
#
# @router.post('/get_vacancy')  # Электрогазосварщик на ВГОК 4, Токарь, Машинист погрузочно-доставочной машины 1
# async def show_vacancy(request: Request, vacancy_name: str = Form(...)):
#     try:
#         vacancy = await get_vacancy(vacancy_name)
#     except Exception as _ex:
#         return templates.TemplateResponse('index.html', {'request': request, 'error': 'not found'})
#     else:
#         return templates.TemplateResponse('index.html',
#                                           {'request': request, 'text': vacancy.text, 'photo_path': vacancy.photo_path,
#                                            'vacancy_name': vacancy.name})
#
#
# @router.post('/regeneration_image')
# async def regeneration_image(request: Request, text: str = Form(...), photo_path: str = Form(...),
#                              vacancy_name: str = Form(...)):
#     photo_path = await generate_image(text.replace('\r', ''), vacancy_name)
#     return templates.TemplateResponse('index.html', {'request': request, 'text': text, 'photo_path': photo_path,
#                                                      'vacancy_name': vacancy_name})
#
#
# @app.post('/send_vacancy')
# async def send_vacancy(request: Request, text: str = Form(...), photo_path: str = Form(...),
#                        vacancy_name: str = Form(...), vk: bool = Form(False), tg: bool = Form(False)):
#     try:
#         if not vk and not tg:
#             raise ValueError
#         await send_vacancy_to_networks(text, photo_path, vk, tg)
#     except Exception as _ex:
#         return templates.TemplateResponse('index.html', {'request': request, 'text': text, 'photo_path': photo_path,
#                                                          'vacancy_name': vacancy_name, 'error': 'error send'})
#     else:
#         return templates.TemplateResponse('index.html', {'request': request, 'msg': 'success send'})
