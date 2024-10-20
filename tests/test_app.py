import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
import io
import json

# Mock the StaticFiles
mock_static_files = MagicMock()

# Patch the StaticFiles import
with patch('fastapi.staticfiles.StaticFiles', return_value=mock_static_files):
    from app.main import app
    from app.config import settings

client = TestClient(app)

def get_auth_client():
    return TestClient(app, headers={"Authorization": f"Bearer {settings.API_KEY}"})

def test_config():
    assert settings.API_KEY != ""
    assert settings.SAAS_API_URL != ""
    assert settings.SECRET_KEY != ""
    assert settings.MAX_FILE_SIZE > 0
    assert len(settings.ALLOWED_EXTENSIONS_SET) > 0
    assert all(ext in settings.ALLOWED_EXTENSIONS_SET for ext in ['csv', 'xlsx', 'pdf', 'docx', 'json'])
    assert settings.MOCK_UPLOAD_SUCCESS == "/file/successUpload"
    assert settings.MOCK_SAAS_API_SUCCESS == "/api/successAPIintegration"
    assert settings.MOCK_SAAS_API_ERROR == "/api/apiErrors"

@pytest.mark.asyncio
async def test_file_upload_csv():
    auth_client = get_auth_client()

    # Mock file handling
    mocked_file_content = "name,email,company,role\nJohn Doe,john@example.com,ACME Inc,Manager"
    
    # Use patch as a context manager
    with patch("app.services.file_handler.handle_file", return_value=mocked_file_content), \
         patch("app.services.data_validator.validate_data", return_value=[
             {"name": "John Doe", "email": "john@example.com", "company": "ACME Inc", "role": "Manager"}
         ]), \
         patch("app.services.data_transformer.transform_data", return_value=[
             {"customer_name": "John Doe", "customer_email": "john@example.com"}
         ]), \
         patch("app.services.saas_api_client.saas_api_client.onboard_customer", new_callable=AsyncMock) as mock_onboard, \
         patch("aiohttp.ClientSession.get") as mock_get:

        # Configure mock responses
        mock_onboard.return_value = {"status": "success"}
        mock_get.return_value.__aenter__.return_value.json.return_value = {"message": "Upload successful"}

        # Perform the test
        csv_content = b"name,email,company,role\nJohn Doe,john@example.com,ACME Inc,Manager"
        files = {"file": ("test.csv", io.BytesIO(csv_content), "text/csv")}
        response = auth_client.post("/onboard", files=files)

        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")

        try:
            print(f"Response JSON: {json.dumps(response.json(), indent=2)}")
        except json.JSONDecodeError:
            print("Response is not JSON decodable")

        assert response.status_code == 200
        assert response.json()["message"] == "Upload successful"
        assert "results" in response.json()
        assert response.json()["results"] == [{"status": "success"}]

        # Verify that the mocked methods were called
        mock_onboard.assert_called_once()
        mock_get.assert_called_once()

# Add more tests as needed