#reason to have a separate file (dependencies.py) that creates the settings instance, which can then be imported by other modules without causing circular dependencies.
from app.config import Settings

settings = Settings()