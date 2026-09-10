import hashlib
import json

from datetime import datetime

# starting hash for the hash chain
GENESIS_HASH = "0" * 64

# for consistent hashing
def canonical_json(data: dict | None) -> str:
    return json.dumps(
        data or {},
        sort_keys=True,
        separators=(",", ":")
    )

#hash fuction - combine audit fields into a string and hash using SHA-256
def compute_audit_hash(
    event_type: str,
    actor_id: int | None,
    visit_id: int | None,
    event_data: str,
    previous_hash: str,
    timestamp: datetime
) -> str:
    payload = (
        f"{event_type}|"
        f"{actor_id}|"
        f"{visit_id}|"
        f"{event_data}|"
        f"{previous_hash}|"
        f"{timestamp.isoformat()}"
    )

    return hashlib.sha256(payload.encode()).hexdigest()