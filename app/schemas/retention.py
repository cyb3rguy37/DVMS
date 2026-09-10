from pydantic import BaseModel


class RetentionCleanupResponse(BaseModel):
    deleted_visitors: int
    affected_visitor_ids: list[int]
    message: str