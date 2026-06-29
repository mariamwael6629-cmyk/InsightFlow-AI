from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(120))
    count: Mapped[int] = mapped_column()
    color: Mapped[str] = mapped_column(String(20))
    rank: Mapped[int] = mapped_column()
