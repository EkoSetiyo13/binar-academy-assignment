from pydantic_settings import BaseSettings
from pathlib import Path
import os

class Settings(BaseSettings):
    APP_NAME: str = "Todo List API"
    API_PREFIX: str = "/api"
    
    # JSON Database configuration
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATABASE_DIR: Path = BASE_DIR / "db"
    DATABASE_FILE: Path = DATABASE_DIR / "data.json"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Ensure database directory exists
os.makedirs(settings.DATABASE_DIR, exist_ok=True)

# Create empty database file if it doesn't exist
if not settings.DATABASE_FILE.exists():
    with open(settings.DATABASE_FILE, "w") as f:
        f.write('{"lists": []}')
