from pydantic import BaseModel, EmailStr, Field


class CompanyProfile(BaseModel):
    name: str
    industry: str
    primary_email: EmailStr
    timezone: str
    website: str
    language: str

    model_config = {"from_attributes": True}


class CompanyProfileUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    industry: str = Field(min_length=1, max_length=120)
    primary_email: EmailStr
    timezone: str = Field(min_length=1, max_length=60)
    website: str = Field(min_length=1, max_length=255)
    language: str = Field(min_length=1, max_length=60)


class PlanInfo(BaseModel):
    plan_name: str
    plan_price: float
    responses_used: int
    responses_limit: int
    seats_used: int
    seats_limit: int


class TeamMemberItem(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    model_config = {"from_attributes": True}


class TeamMemberInvite(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    role: str = Field(default="viewer", pattern="^(admin|editor|viewer)$")


class TeamMemberInviteResponse(TeamMemberItem):
    temporary_password: str


class NotificationSettingItem(BaseModel):
    key: str
    label: str
    description: str
    enabled: bool

    model_config = {"from_attributes": True}


class NotificationSettingUpdate(BaseModel):
    enabled: bool
