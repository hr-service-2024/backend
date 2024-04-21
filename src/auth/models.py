from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.auth.schemas import UserSchema


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            username=self.username,
            hashed_password=self.hashed_password,
            is_active=self.is_active
        )
