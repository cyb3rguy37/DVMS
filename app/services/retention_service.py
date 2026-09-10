from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import AuditEventType, Visitor
from app.schemas import RetentionCleanupResponse
from app.services.audit_service import create_audit_event

#remove expired visitor PII while preserving visit/audit history
def cleanup_expired_visitors_service(
    db: Session,
    actor_id: int
) -> RetentionCleanupResponse:
    expired_visitors = (
        db.query(Visitor)
        .filter(Visitor.retention_expiry != None)
        .filter(Visitor.retention_expiry <= datetime.utcnow())
        .all()
    )

    affected_ids = []

    for visitor in expired_visitors:
        affected_ids.append(visitor.id)

        #destory personal data while preserving the visitor record
        visitor.encrypted_name = "[DELETED]"
        visitor.encrypted_phone = "[DELETED]"
        visitor.encrypted_id_number = "[DELETED]"
        visitor.phone_blind_index = None
        visitor.id_blind_index = None

    db.commit()

    create_audit_event(
        db=db,
        event_type=AuditEventType.RETENTION_DELETE,
        actor_id=actor_id,
        event_data={
            "deleted_visitors": len(affected_ids),
            "visitor_ids": affected_ids
        }
    )

    return RetentionCleanupResponse(
        deleted_visitors=len(affected_ids),
        affected_visitor_ids=affected_ids,
        message="Retention cleanup completed successfully"
    )