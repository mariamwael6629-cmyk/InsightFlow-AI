from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import get_current_user
from app.schemas.reports import ComparisonRow, ReportItem
from app.services import reports_service

router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[ReportItem])
def list_reports(db: Session = Depends(get_db)):
    return reports_service.get_reports(db)


@router.get("/comparison", response_model=list[ComparisonRow])
def comparison(db: Session = Depends(get_db)):
    return reports_service.get_comparison(db)
