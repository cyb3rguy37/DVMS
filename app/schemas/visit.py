from datetime import datetime

from pydantic import BaseModel

from app.db.models import VisitStatus


class VisitCheckoutResponse(BaseModel):
    visit_id: int
    status: VisitStatus
    check_in_time: datetime
    check_out_time: datetime
    message: str


class ActiveVisitResponse(BaseModel):
    visit_id: int
    visitor_id: int
    masked_name: str
    masked_phone: str | None
    host_name: str
    purpose: str | None
    check_in_time: datetime
    status: VisitStatus