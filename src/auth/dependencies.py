from src.auth.service import UserService
from src.auth.repositories import UserRepository


def get_user_service():
    return UserService(UserRepository)
