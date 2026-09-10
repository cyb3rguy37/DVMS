from pydantic import BaseModel


class AuditVerificationResponse(BaseModel):
    valid: bool
    broken_at_event_id: int | None = None
    message: str