from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.auth.schemas import UserSchema


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    hashtag: Mapped[str] = mapped_column(default='')
    specialist: Mapped[str] = mapped_column(default='')
    phone: Mapped[str] = mapped_column(default='')
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
            is_active=self.is_active,
            is_superuser=self.is_superuser
        )
