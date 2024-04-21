from pydantic import BaseModel


class ShowVacancy(BaseModel):
    name: str
    text: str
    photo_path: str
