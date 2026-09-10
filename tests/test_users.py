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


def test_admin_can_create_guard_user(client):
    headers = login_admin(client)

    response = client.post(
        "/admin/users",
        headers=headers,
        json={
            "username": "guard1",
            "password": "GuardPass123!",
            "role": "guard"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "guard1"
    assert data["role"] == "guard"
    assert data["is_active"] is True


def test_duplicate_username_rejected(client):
    headers = login_admin(client)

    payload = {
        "username": "guard1",
        "password": "GuardPass123!",
        "role": "guard"
    }

    first_response = client.post(
        "/admin/users",
        headers=headers,
        json=payload
    )

    second_response = client.post(
        "/admin/users",
        headers=headers,
        json=payload
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Username already exists"


def test_create_user_requires_authentication(client):
    response = client.post(
        "/admin/users",
        json={
            "username": "guard2",
            "password": "GuardPass123!",
            "role": "guard"
        }
    )

    assert response.status_code == 401

#RBAC Test 
def login_user(client, username: str, password: str):
    response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_guard_cannot_create_user(client):
    admin_headers = login_admin(client)

    client.post(
        "/admin/users",
        headers=admin_headers,
        json={
            "username": "guard1",
            "password": "GuardPass123!",
            "role": "guard"
        }
    )

    guard_headers = login_user(
        client,
        username="guard1",
        password="GuardPass123!"
    )

    response = client.post(
        "/admin/users",
        headers=guard_headers,
        json={
            "username": "guard2",
            "password": "GuardPass123!",
            "role": "guard"
        }
    )

    assert response.status_code == 403