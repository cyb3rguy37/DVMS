from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.database import get_db
from app.db.models import AuditEventType, User, UserRole
from app.schemas import AuditVerificationResponse
from app.services.audit_service import create_audit_event, verify_audit_chain


router = APIRouter(
    prefix="/audit",
    tags=["Audit"]
)


@router.get("/verify", response_model=AuditVerificationResponse)
def verify_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.AUDITOR))
):
    valid, broken_id = verify_audit_chain(db)

    create_audit_event(
        db=db,
        event_type=AuditEventType.VERIFY_AUDIT_CHAIN,
        actor_id=current_user.id,
        event_data={
            "valid": valid,
            "broken_at": broken_id
        }
    )

    if valid:
        return AuditVerificationResponse(
            valid=True,
            broken_at_event_id=None,
            message="Audit chain is valid"
        )

    return AuditVerificationResponse(
        valid=False,
        broken_at_event_id=broken_id,
        message="Audit chain integrity failure detected"
    )