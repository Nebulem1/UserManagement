import pytest


@pytest.fixture
def normal_user_token(client):
    client.post(
        "/auth/register",
        json={
            "username": "users_test",
            "email": "utest@example.com",
            "password": "abc",
        },
    )
    r = client.post("/auth/login", data={"username": "users_test", "password": "abc"})
    return r.json()["access_token"]


def test_read_users_me(client, normal_user_token):
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {normal_user_token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "users_test"


def test_change_password(client, normal_user_token):
    response = client.put(
        "/users/change-password",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"current_password": "abc", "new_password": "newpassword"},
    )
    assert response.status_code == 200

    # Try login with new
    r = client.post(
        "/auth/login", data={"username": "users_test", "password": "newpassword"}
    )
    assert r.status_code == 200
    # Try login with old
    r2 = client.post("/auth/login", data={"username": "users_test", "password": "abc"})
    assert r2.status_code == 401
