from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, String

from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)