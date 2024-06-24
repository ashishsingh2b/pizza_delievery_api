import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from database import Session, engine, Base
from main import app  # Assuming your FastAPI app instance is named `app`

# Create a test database and session
@pytest.fixture(scope="module")
def override_get_db():
    # Use a temporary SQLite database for testing
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    # Establish a new session for the test
    session = TestingSessionLocal()

    # Create all tables
    Base.metadata.create_all(bind=engine)

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(override_get_db):
    def _get_test_db():
        return override_get_db

    # Provide the override_get_db function to FastAPI's dependency resolver
    app.dependency_overrides[Session] = _get_test_db

    # Create a test client using the provided FastAPI app
    with TestClient(app) as c:
        yield c

# Test cases for each endpoint
def test_hello(client):
    response = client.get("/orders/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_place_an_order(client):
    order_data = {"quantity": 2, "pizza_size": "large"}
    response = client.post("/orders/order", json=order_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_list_all_orders(client):
    response = client.get("/orders/orders")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_order_by_id(client):
    response = client.get("/orders/orders/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_user_orders(client):
    response = client.get("/orders/user/orders")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_specific_order(client):
    response = client.get("/orders/user/order/1/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_update_order(client):
    order_data = {"quantity": 3, "pizza_size": "medium"}
    response = client.put("/orders/order/update/1/", json=order_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_update_order_status(client):
    order_status_data = {"order_status": "completed"}
    response = client.patch("/orders/order/update/1/", json=order_status_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_an_order(client):
    response = client.delete("/orders/order/delete/1/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
