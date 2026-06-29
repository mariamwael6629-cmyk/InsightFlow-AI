from datetime import date

from pydantic import BaseModel


class MetricCard(BaseModel):
    label: str
    value: str
    delta: str
    trend: str  # up | down


class MetricsResponse(BaseModel):
    total_responses: MetricCard
    avg_sentiment: MetricCard
    issues_flagged: MetricCard
    ai_suggestions: MetricCard


class TrendPoint(BaseModel):
    stat_date: date
    positive_pct: float
    neutral_pct: float
    negative_pct: float

    model_config = {"from_attributes": True}


class CategoryItem(BaseModel):
    category: str
    percentage: float
    color: str

    model_config = {"from_attributes": True}


class HeatmapCell(BaseModel):
    week_index: int
    day_index: int
    score: int

    model_config = {"from_attributes": True}


class IssueItem(BaseModel):
    rank: int
    label: str
    count: int
    color: str

    model_config = {"from_attributes": True}


class RecommendationItem(BaseModel):
    priority: str
    title: str
    detail: str

    model_config = {"from_attributes": True}
