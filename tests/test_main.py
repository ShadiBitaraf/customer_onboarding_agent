# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import settings  # Updated import

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Customer Onboarding Agent"}

def test_onboard_customer():
    # This is a basic test. You'll need to mock the file upload and API calls for a more comprehensive test.
    files = {"file": ("test.csv", "name,email,company,role\nJohn Doe,john@example.com,ACME Inc,Manager")}
    response = client.post("/onboard", files=files)
    assert response.status_code == 200
    assert "message" in response.json()
    assert "results"