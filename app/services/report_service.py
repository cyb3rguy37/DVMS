from sqlalchemy.orm import Session

from app.db.models import Visit, VisitStatus
from app.schemas import ReportSummaryResponse


#create a simple report (all, active and checked-out visits)
def get_report_summary_service(
    db: Session
) -> ReportSummaryResponse:
    visits = db.query(Visit).all()

    total_visits = len(visits)

    active_visits = len([
        visit for visit in visits
        if visit.status == VisitStatus.ACTIVE
    ])

    checked_out_visits = len([
        visit for visit in visits
        if visit.status == VisitStatus.CHECKED_OUT
    ])

    return ReportSummaryResponse(
        total_visits=total_visits,
        active_visits=active_visits,
        checked_out_visits=checked_out_visits
    )