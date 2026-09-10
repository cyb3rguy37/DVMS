import hashlib
import hmac

from app.core.config import settings

#convert equivalent values to a consistent format
def normalize_identifier(value: str | None) -> str | None:
    if value is None or value == "":
        return None

    return value.strip().lower().replace(" ", "").replace("-", "")

def create_blind_index(value: str | None) -> str | None:
    normalized = normalize_identifier(value)

    if normalized is None:
        return None

    digest = hmac.new(
        settings.blind_index_pepper.encode(),
        normalized.encode(),
        hashlib.sha256
    ).hexdigest()

    return digest