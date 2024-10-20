# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Set


class Settings(BaseSettings):
    API_KEY: str
    SAAS_API_URL: str
    SECRET_KEY: str
    MAX_FILE_SIZE: int
    ALLOWED_EXTENSIONS: str

    # Mock paths
    MOCK_AUTH_SUCCESS: str = "/auth/success"
    MOCK_AUTH_INVALID_USERNAME: str = "/auth/invalidUsername"
    MOCK_AUTH_INVALID_PASSWORD: str = "/auth/invalidpass"
    MOCK_UPLOAD_SUCCESS: str = "/file/successUpload"
    MOCK_INVALID_FILE_TYPE: str = "/file/invalidType"
    MOCK_FILE_SIZE_LIMIT: str = "/file/sizeExceeded"
    MOCK_DATA_VALIDATION_ERROR: str = "/file/validationError"
    MOCK_SAAS_API_SUCCESS: str = "/api/successAPIintegration"
    MOCK_SAAS_API_ERROR: str = "/api/apiErrors"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def ALLOWED_EXTENSIONS_SET(self) -> Set[str]:
        return set(self.ALLOWED_EXTENSIONS.split(","))


settings = Settings()
