from datetime import datetime

from pydantic import BaseModel, Field

from app.db.models import VisitStatus


class VisitorRegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    phone_number: str | None = Field(default=None, max_length=30)
    id_number: str | None = Field(default=None, max_length=50)
    host_name: str = Field(min_length=2, max_length=150)
    purpose: str | None = Field(default=None, max_length=255)
    consent_given: bool


class VisitorRegisterResponse(BaseModel):
    visitor_id: int
    visit_id: int
    masked_name: str
    masked_phone: str | None
    host_name: str
    status: VisitStatus
    check_in_time: datetime