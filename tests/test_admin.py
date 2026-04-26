import pytest

from app.models.user import User


@pytest.fixture
def normal_user_token(client):
    client.post(
        "/auth/register",
        json={"username": "norm_adm", "email": "n@example.com", "password": "123"},
    )
    r = client.post("/auth/login", data={"username": "norm_adm", "password": "123"})
    return r.json()["access_token"]


@pytest.fixture
def admin_user_token(client, db_session):
    client.post(
        "/auth/register",
        json={"username": "admin_user", "email": "a@example.com", "password": "123"},
    )
    r = client.post("/auth/login", data={"username": "admin_user", "password": "123"})
    token = r.json()["access_token"]

    # Escalate role via DB
    user = db_session.query(User).filter_by(username="admin_user").first()
    user.role = "admin"
    db_session.commit()
    db_session.refresh(user)
    return token


def test_normal_user_blocked_from_admin(client, normal_user_token):
    response = client.get(
        "/admin/users", headers={"Authorization": f"Bearer {normal_user_token}"}
    )
    assert response.status_code == 403


def test_admin_can_list_users(client, admin_user_token):
    response = client.get(
        "/admin/users", headers={"Authorization": f"Bearer {admin_user_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1
