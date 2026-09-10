from pydantic import BaseModel


class ReportSummaryResponse(BaseModel):
    total_visits: int
    active_visits: int
    checked_out_visits: int