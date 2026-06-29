from datetime import date

from sqlalchemy import Date, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SentimentDailyStat(Base):
    """Aggregated daily sentiment percentages, used to render the trend chart."""

    __tablename__ = "sentiment_daily_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    stat_date: Mapped[date] = mapped_column(Date, index=True)
    positive_pct: Mapped[float] = mapped_column(Float)
    neutral_pct: Mapped[float] = mapped_column(Float)
    negative_pct: Mapped[float] = mapped_column(Float)


class CategoryBreakdown(Base):
    """Share of feedback volume per topic category (Product, Support, UX, Pricing...)."""

    __tablename__ = "category_breakdowns"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(60))
    percentage: Mapped[float] = mapped_column(Float)
    color: Mapped[str] = mapped_column(String(20))


class MoodHeatmapCell(Base):
    """One cell of the 5-week x 7-day customer mood heatmap, score 0-9."""

    __tablename__ = "mood_heatmap_cells"

    id: Mapped[int] = mapped_column(primary_key=True)
    week_index: Mapped[int] = mapped_column()
    day_index: Mapped[int] = mapped_column()  # 0=Mon ... 6=Sun
    score: Mapped[int] = mapped_column()
