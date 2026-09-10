from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.database import get_db
from app.db.models import User, UserRole
from app.schemas import ReportSummaryResponse
from app.services.report_service import get_report_summary_service


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/summary", response_model=ReportSummaryResponse)
def get_report_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.AUDITOR))
):
    return get_report_summary_service(db=db)