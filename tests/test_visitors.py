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

def test_register_visitor_success(client):
    headers = login_admin(client)

    response = register_sample_visitor(client, headers)

    assert response.status_code == 200

    data = response.json()

    assert data["visitor_id"] == 1
    assert data["visit_id"] == 1
    assert data["masked_name"] == "Ja******"
    assert data["masked_phone"] == "07********"
    assert data["status"] == "active"

#consent rejection test 
def test_register_visitor_requires_consent(client):
    headers = login_admin(client)

    response = client.post(
        "/visitors/register",
        headers=headers,
        json={
            "full_name": "No Consent Visitor",
            "phone_number": "0711111111",
            "id_number": "11111111",
            "host_name": "Reception",
            "purpose": "Inquiry",
            "consent_given": False
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Visitor consent is required"

    #test visitor search, checkout, and active visitors tests.
def test_search_visitor_by_phone(client):
    headers = login_admin(client)

    register_sample_visitor(client, headers)

    response = client.get(
        "/visitors/search?phone_number=0712345678",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["masked_name"] == "Ja******"
    assert data[0]["masked_phone"] == "07********"


def test_checkout_visitor(client):
    headers = login_admin(client)

    register_response = register_sample_visitor(client, headers)
    visit_id = register_response.json()["visit_id"]

    response = client.post(
        f"/visits/{visit_id}/checkout",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["visit_id"] == visit_id
    assert data["status"] == "checked_out"


def test_active_visitors(client):
    headers = login_admin(client)

    register_sample_visitor(client, headers)

    response = client.get(
        "/visits/active",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["status"] == "active"