from datetime import date

from pydantic import BaseModel


class ReportItem(BaseModel):
    id: int
    title: str
    description: str
    icon: str
    icon_bg: str
    report_date: date

    model_config = {"from_attributes": True}


class ComparisonRow(BaseModel):
    metric_name: str
    previous_label: str
    previous_display: str
    previous_value: float
    current_label: str
    current_display: str
    current_value: float
    trend: str

    model_config = {"from_attributes": True}
