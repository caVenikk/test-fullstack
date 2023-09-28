from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from src.utils.base import Base


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    image: Mapped[bytes] = mapped_column(LargeBinary())
    description: Mapped[str]
