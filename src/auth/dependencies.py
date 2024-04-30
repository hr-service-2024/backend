from src.auth.service import UserService, ChannelService
from src.auth.repositories import UserRepository, TgChannelRepository, VkChannelRepository


def get_user_service():
    return UserService(UserRepository)


def get_tg_channel_service():
    return ChannelService(TgChannelRepository)


def get_vk_channel_service():
    return ChannelService(VkChannelRepository)
