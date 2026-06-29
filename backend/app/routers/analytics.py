from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import get_current_user
from app.schemas.analytics import (
    CategoryItem,
    HeatmapCell,
    IssueItem,
    MetricsResponse,
    RecommendationItem,
    TrendPoint,
)
from app.services import analytics_service

router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/metrics", response_model=MetricsResponse)
def metrics(db: Session = Depends(get_db)):
    return analytics_service.get_metrics(db)


@router.get("/trend", response_model=list[TrendPoint])
def trend(db: Session = Depends(get_db)):
    return analytics_service.get_trend(db)


@router.get("/categories", response_model=list[CategoryItem])
def categories(db: Session = Depends(get_db)):
    return analytics_service.get_categories(db)


@router.get("/heatmap", response_model=list[HeatmapCell])
def heatmap(db: Session = Depends(get_db)):
    return analytics_service.get_heatmap(db)


@router.get("/issues", response_model=list[IssueItem])
def issues(db: Session = Depends(get_db)):
    return analytics_service.get_issues(db)


@router.get("/recommendations", response_model=list[RecommendationItem])
def recommendations(db: Session = Depends(get_db)):
    return analytics_service.get_recommendations(db)
