import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app, get_db
import models

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Apply the override
app.dependency_overrides[get_db] = override_get_db

# Create the test client
client = TestClient(app)

# Set up the test database
@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_transaction():
    response = client.post("/transactions/", json={
        "amount": 100.0,
        "category": "Food",
        "description": "Grocery shopping",
        "is_income": False,
        "date": "2024-08-29"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 100.0
    assert data["category"] == "Food"
    assert data["description"] == "Grocery shopping"
    assert data["is_income"] == False
    assert data["date"] == "2024-08-29"
    assert "id" in data

def test_read_transactions():
    # Add a transaction to the database
    client.post("/transactions/", json={
        "amount": 50.0,
        "category": "Transport",
        "description": "Bus fare",
        "is_income": False,
        "date": "2024-08-28"
    })
    
    response = client.get("/transactions/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["amount"] == 50.0
    assert data[0]["category"] == "Transport"
    assert data[0]["description"] == "Bus fare"
    assert data[0]["is_income"] == False
    assert data[0]["date"] == "2024-08-28"
