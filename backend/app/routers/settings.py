from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import get_current_user
from app.models.user import User
from app.schemas.settings import (
    CompanyProfile,
    CompanyProfileUpdate,
    NotificationSettingItem,
    NotificationSettingUpdate,
    PlanInfo,
    TeamMemberInvite,
    TeamMemberInviteResponse,
    TeamMemberItem,
)
from app.services import settings_service

router = APIRouter(
    prefix="/api/settings",
    tags=["Settings"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/company", response_model=CompanyProfile)
def get_company(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return settings_service.get_company(db, current_user.company_id)


@router.put("/company", response_model=CompanyProfile)
def update_company(
    payload: CompanyProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return settings_service.update_company(db, current_user.company_id, payload)


@router.get("/plan", response_model=PlanInfo)
def get_plan(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    company = settings_service.get_company(db, current_user.company_id)
    return PlanInfo(
        plan_name=company.plan_name,
        plan_price=company.plan_price,
        responses_used=company.responses_used,
        responses_limit=company.responses_limit,
        seats_used=company.seats_used,
        seats_limit=company.seats_limit,
    )


@router.get("/team", response_model=list[TeamMemberItem])
def list_team(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return settings_service.list_team_members(db, current_user.company_id)


@router.post("/team", response_model=TeamMemberInviteResponse, status_code=status.HTTP_201_CREATED)
def invite_team_member(
    payload: TeamMemberInvite,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    member, temp_password = settings_service.invite_team_member(db, current_user.company_id, payload)
    return TeamMemberInviteResponse(
        id=member.id,
        name=member.name,
        email=member.email,
        role=member.role,
        temporary_password=temp_password,
    )


@router.delete("/team/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_team_member(
    member_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    settings_service.remove_team_member(db, current_user.company_id, member_id)


@router.get("/notifications", response_model=list[NotificationSettingItem])
def list_notifications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return settings_service.list_notification_settings(db, current_user.company_id)


@router.put("/notifications/{key}", response_model=NotificationSettingItem)
def update_notification(
    key: str,
    payload: NotificationSettingUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return settings_service.update_notification_setting(db, current_user.company_id, key, payload.enabled)
