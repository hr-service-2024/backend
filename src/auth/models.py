from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List

from src.database import Base
from src.auth.schemas import UserSchema, ChannelSchema


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    hashtag: Mapped[str] = mapped_column(default='')
    specialist: Mapped[str] = mapped_column(default='')
    phone: Mapped[str] = mapped_column(default='')
    tg_channels: Mapped[List['TgChannel']] = relationship(back_populates='user', lazy='selectin')
    vk_channels: Mapped[List['VkChannel']] = relationship(back_populates='user', lazy='selectin')
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            username=self.username,
            hashed_password=self.hashed_password,
            hashtag=self.hashtag,
            specialist=self.specialist,
            phone=self.phone,
            tg_channels=self.tg_channels,
            vk_channels=self.vk_channels,
            is_active=self.is_active,
            is_superuser=self.is_superuser
        )


class TgChannel(Base):
    __tablename__ = 'tg_channels'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='cascade'), nullable=False, index=True)
    user: Mapped['User'] = relationship(back_populates='tg_channels')

    def to_read_model(self) -> ChannelSchema:
        return ChannelSchema(
            id=self.id,
            user_id=self.user_id
        )


class VkChannel(Base):
    __tablename__ = 'vk_channels'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='cascade'), nullable=False, index=True)
    user: Mapped['User'] = relationship(back_populates='vk_channels')

    def to_read_model(self) -> ChannelSchema:
        return ChannelSchema(
            id=self.id,
            user_id=self.user_id
        )
