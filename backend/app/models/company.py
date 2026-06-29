from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), default="Acme Corp")
    industry: Mapped[str] = mapped_column(String(120), default="E-Commerce / Retail")
    primary_email: Mapped[str] = mapped_column(String(255), default="team@acmecorp.com")
    timezone: Mapped[str] = mapped_column(String(60), default="UTC+0 — London")
    website: Mapped[str] = mapped_column(String(255), default="https://acmecorp.com")
    language: Mapped[str] = mapped_column(String(60), default="English (UK)")
    plan_name: Mapped[str] = mapped_column(String(30), default="Pro")
    plan_price: Mapped[float] = mapped_column(default=89.0)
    responses_used: Mapped[int] = mapped_column(default=7234)
    responses_limit: Mapped[int] = mapped_column(default=10000)
    seats_used: Mapped[int] = mapped_column(default=3)
    seats_limit: Mapped[int] = mapped_column(default=5)

    users: Mapped[list["User"]] = relationship(back_populates="company")  # noqa: F821
