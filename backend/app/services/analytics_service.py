from sqlalchemy.orm import Session

from app.models.feedback import CategoryBreakdown, MoodHeatmapCell, SentimentDailyStat
from app.models.issue import Issue
from app.models.recommendation import Recommendation
from app.schemas.analytics import MetricCard, MetricsResponse


def get_metrics(db: Session) -> MetricsResponse:
    return MetricsResponse(
        total_responses=MetricCard(label="Total Responses", value="12,847", delta="↑ 18% vs prior period", trend="up"),
        avg_sentiment=MetricCard(label="Avg Sentiment Score", value="8.7", delta="↑ +0.4 pts improvement", trend="up"),
        issues_flagged=MetricCard(label="Issues Flagged", value="47", delta="↓ 12 new this week", trend="down"),
        ai_suggestions=MetricCard(label="AI Suggestions", value="23", delta="↑ 5 high-priority new", trend="up"),
    )


def get_trend(db: Session) -> list[SentimentDailyStat]:
    return db.query(SentimentDailyStat).order_by(SentimentDailyStat.stat_date).all()


def get_categories(db: Session) -> list[CategoryBreakdown]:
    return db.query(CategoryBreakdown).order_by(CategoryBreakdown.percentage.desc()).all()


def get_heatmap(db: Session) -> list[MoodHeatmapCell]:
    return (
        db.query(MoodHeatmapCell)
        .order_by(MoodHeatmapCell.week_index, MoodHeatmapCell.day_index)
        .all()
    )


def get_issues(db: Session) -> list[Issue]:
    return db.query(Issue).order_by(Issue.rank).all()


def get_recommendations(db: Session) -> list[Recommendation]:
    return db.query(Recommendation).all()
