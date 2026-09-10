from datetime import datetime

from app.utils.hash_chain import GENESIS_HASH, canonical_json, compute_audit_hash

timestamp = datetime.utcnow()

event_data = canonical_json({
    "visitor_id": 1,
    "action": "register_visitor"
})

hash_1 = compute_audit_hash(
    event_type="register_visitor",
    actor_id=1,
    visit_id=1,
    event_data=event_data,
    previous_hash=GENESIS_HASH,
    timestamp=timestamp
)

hash_2 = compute_audit_hash(
    event_type="register_visitor",
    actor_id=1,
    visit_id=1,
    event_data=event_data,
    previous_hash=GENESIS_HASH,
    timestamp=timestamp
)

print(hash_1)
print(hash_2)
print(hash_1 == hash_2)