import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.vacancies.router import router as vacancies_router


app = FastAPI(title='HR-service')
app.include_router(auth_router)
app.include_router(vacancies_router)

# CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(app)
