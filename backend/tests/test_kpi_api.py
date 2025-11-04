"""Example tests for KPI API endpoints.

Run with: pytest backend/tests/test_kpi_api.py
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.core.security import get_password_hash

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    """Create test database."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    """Create test client."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def test_user(db):
    """Create test user."""
    from app.models.user import User
    user = User(
        email="test@example.com",
        full_name="Test User",
        hashed_password=get_password_hash("testpass123"),
        role="employee",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "testpass123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_kpi(client, auth_headers):
    """Test creating a KPI."""
    response = client.post(
        "/api/v1/kpis",
        json={
            "title": "Test KPI",
            "year": 2024,
            "quarter": "Q1",
            "target_value": "100",
            "progress_percentage": 50
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test KPI"
    assert data["year"] == 2024
    assert data["quarter"] == "Q1"


def test_list_kpis(client, auth_headers):
    """Test listing KPIs."""
    # Create a KPI first
    client.post(
        "/api/v1/kpis",
        json={"title": "Test KPI", "year": 2024, "quarter": "Q1"},
        headers=auth_headers
    )

    # List KPIs
    response = client.get("/api/v1/kpis", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1


def test_unauthorized_access(client):
    """Test unauthorized access is blocked."""
    response = client.get("/api/v1/kpis")
    assert response.status_code == 401
