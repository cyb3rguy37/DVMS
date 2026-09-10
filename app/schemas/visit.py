from datetime import datetime

from pydantic import BaseModel

from app.db.models import VisitStatus


class VisitCheckoutResponse(BaseModel):
    visit_id: int
    status: VisitStatus
    check_in_time: datetime
    check_out_time: datetime
    message: str