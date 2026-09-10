from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import AuditEventType, Visit, VisitStatus, Visitor
from app.schemas import ActiveVisitResponse, VisitCheckoutResponse
from app.services.audit_service import create_audit_event
from app.utils.encryption import decrypt_value, mask_text


def checkout_visit_service(
    db: Session,
    visit_id: int,
    actor_id: int
) -> VisitCheckoutResponse:
    visit = db.query(Visit).filter(Visit.id == visit_id).first()

    if not visit:
        raise HTTPException(
            status_code=404,
            detail="Visit not found"
        )

    if visit.status != VisitStatus.ACTIVE:
        raise HTTPException(
            status_code=400,
            detail="Visitor is already checked out"
        )

    visit.status = VisitStatus.CHECKED_OUT
    visit.check_out_time = datetime.utcnow()

    db.commit()
    db.refresh(visit)

    create_audit_event(
        db=db,
        event_type=AuditEventType.CHECK_OUT,
        actor_id=actor_id,
        visit_id=visit.id,
        event_data={
            "visitor_id": visit.visitor_id
        }
    )

    return VisitCheckoutResponse(
        visit_id=visit.id,
        status=visit.status,
        check_in_time=visit.check_in_time,
        check_out_time=visit.check_out_time,
        message="Visitor checked out successfully"
    )

#find active visitors and return masked values
def get_active_visits_service(
    db: Session
) -> list[ActiveVisitResponse]:
    visits = (
        db.query(Visit)
        .filter(Visit.status == VisitStatus.ACTIVE)
        .order_by(Visit.check_in_time.desc())
        .all()
    )

    results = []

    for visit in visits:
        visitor = db.query(Visitor).filter(Visitor.id == visit.visitor_id).first()

        if visitor:
            name = decrypt_value(visitor.encrypted_name)
            phone = decrypt_value(visitor.encrypted_phone)

            results.append(
                ActiveVisitResponse(
                    visit_id=visit.id,
                    visitor_id=visitor.id,
                    masked_name=mask_text(name),
                    masked_phone=mask_text(phone),
                    host_name=visit.host_name,
                    purpose=visit.purpose,
                    check_in_time=visit.check_in_time,
                    status=visit.status
                )
            )

    return results