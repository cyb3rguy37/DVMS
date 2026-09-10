def test_login_success(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "AdminPass123!"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_failure_wrong_password(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401


def test_auth_me_success(client):
    login_response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "AdminPass123!"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "admin"
    assert data["role"] == "admin"


def test_auth_me_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401