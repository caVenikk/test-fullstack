from sqlalchemy.orm import Mapped, mapped_column

from src.utils.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)

    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    is_admin: Mapped[bool] = mapped_column(default=False)
