from datetime import datetime, timedelta

from tests.conftest import TestingSessionLocal
from app.db.models import Visitor


def login_admin(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "AdminPass123!"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def register_sample_visitor(client, headers):
    response = client.post(
        "/visitors/register",
        headers=headers,
        json={
            "full_name": "Jane Doe",
            "phone_number": "0712345678",
            "id_number": "12345678",
            "host_name": "ICT Office",
            "purpose": "Meeting",
            "consent_given": True
        }
    )

    return response

def test_audit_verification_success(client):
    headers = login_admin(client)

    register_sample_visitor(client, headers)

    response = client.get(
        "/audit/verify",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["valid"] is True
    assert data["broken_at_event_id"] is None
    assert data["message"] == "Audit chain is valid"


#retention cleanup test
def test_retention_cleanup_deletes_expired_pii(client):
    headers = login_admin(client)

    register_sample_visitor(client, headers)

    db = TestingSessionLocal()

    visitor = db.query(Visitor).first()
    visitor.retention_expiry = datetime.utcnow() - timedelta(days=1)

    db.commit()
    db.close()

    response = client.post(
        "/retention/cleanup",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["deleted_visitors"] == 1
    assert data["affected_visitor_ids"] == [1]

    db = TestingSessionLocal()

    visitor = db.query(Visitor).first()

    assert visitor.encrypted_name == "[DELETED]"
    assert visitor.encrypted_phone == "[DELETED]"
    assert visitor.encrypted_id_number == "[DELETED]"
    assert visitor.phone_blind_index is None
    assert visitor.id_blind_index is None

    db.close()