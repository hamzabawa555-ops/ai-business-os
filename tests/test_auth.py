"""Authentication Tests"""

def test_login(client, sample_user_data):
    """Test user login"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_register(client, sample_user_data):
    """Test user registration"""
    response = client.post(
        "/api/v1/auth/register",
        json=sample_user_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == sample_user_data["email"]
    assert data["first_name"] == sample_user_data["first_name"]

def test_logout(client):
    """Test user logout"""
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
