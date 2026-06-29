from sqlalchemy.orm import Session

from app.models.report import ComparisonMetric, Report


def get_reports(db: Session) -> list[Report]:
    return db.query(Report).order_by(Report.report_date.desc()).all()


def get_comparison(db: Session) -> list[ComparisonMetric]:
    return db.query(ComparisonMetric).all()
