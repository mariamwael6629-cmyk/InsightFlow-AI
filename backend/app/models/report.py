from datetime import date

from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(160))
    description: Mapped[str] = mapped_column(Text)
    icon: Mapped[str] = mapped_column(String(10))
    icon_bg: Mapped[str] = mapped_column(String(30))
    report_date: Mapped[date] = mapped_column(Date)


class ComparisonMetric(Base):
    """Month-over-month performance comparison row used in the Reports page."""

    __tablename__ = "comparison_metrics"

    id: Mapped[int] = mapped_column(primary_key=True)
    metric_name: Mapped[str] = mapped_column(String(60))
    previous_label: Mapped[str] = mapped_column(String(30))
    previous_value: Mapped[float] = mapped_column()
    previous_display: Mapped[str] = mapped_column(String(30))
    current_label: Mapped[str] = mapped_column(String(30))
    current_value: Mapped[float] = mapped_column()
    current_display: Mapped[str] = mapped_column(String(30))
    trend: Mapped[str] = mapped_column(String(10))  # up | down
