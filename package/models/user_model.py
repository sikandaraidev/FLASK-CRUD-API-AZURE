from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from package.azure_database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
