def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_register_duplicate_email(client):
    client.post(
        "/auth/register",
        json={"username": "testuser1", "email": "dup@example.com", "password": "p"},
    )
    response = client.post(
        "/auth/register",
        json={"username": "testuser2", "email": "dup@example.com", "password": "p"},
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_login_success(client):
    # Ensure there's a user
    client.post(
        "/auth/register",
        json={"username": "logintest", "email": "login@example.com", "password": "pwd"},
    )
    response = client.post(
        "/auth/login",
        data={
            "username": "logintest",
            "password": "pwd",
        },  # OAuth2PasswordRequestForm uses form data
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={"username": "failtest", "email": "fail@example.com", "password": "pwd"},
    )
    response = client.post(
        "/auth/login", data={"username": "failtest", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_access_protected_route_without_token(client):
    response = client.get("/auth/me")
    assert response.status_code == 401
