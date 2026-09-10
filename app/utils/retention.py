from datetime import datetime, timedelta

#retention function
def calculate_retention_expiry(days: int = 180) -> datetime:
    return datetime.utcnow() + timedelta(days=days)
