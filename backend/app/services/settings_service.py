import secrets

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.company import Company
from app.models.notification_setting import NotificationSetting
from app.models.user import User
from app.schemas.settings import CompanyProfileUpdate, TeamMemberInvite


def get_company(db: Session, company_id: int) -> Company:
    company = db.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company


def update_company(db: Session, company_id: int, payload: CompanyProfileUpdate) -> Company:
    company = get_company(db, company_id)
    for field, value in payload.model_dump().items():
        setattr(company, field, value)
    db.commit()
    db.refresh(company)
    return company


def list_team_members(db: Session, company_id: int) -> list[User]:
    return db.query(User).filter(User.company_id == company_id).all()


def invite_team_member(db: Session, company_id: int, payload: TeamMemberInvite) -> tuple[User, str]:
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already invited")

    temp_password = secrets.token_urlsafe(9)
    user = User(
        name=payload.name,
        email=payload.email,
        role=payload.role,
        hashed_password=hash_password(temp_password),
        company_id=company_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user, temp_password


def remove_team_member(db: Session, company_id: int, member_id: int) -> None:
    member = db.query(User).filter(User.id == member_id, User.company_id == company_id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found")
    db.delete(member)
    db.commit()


def list_notification_settings(db: Session, company_id: int) -> list[NotificationSetting]:
    return db.query(NotificationSetting).filter(NotificationSetting.company_id == company_id).all()


def update_notification_setting(
    db: Session, company_id: int, key: str, enabled: bool
) -> NotificationSetting:
    setting = (
        db.query(NotificationSetting)
        .filter(NotificationSetting.company_id == company_id, NotificationSetting.key == key)
        .first()
    )
    if not setting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification setting not found")
    setting.enabled = enabled
    db.commit()
    db.refresh(setting)
    return setting
