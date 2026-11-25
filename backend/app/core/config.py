import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")

    PROJECT_NAME: str = "ENCUÉNTRAME NICARAGUA"
    PROJECT_DESCRIPTION: str = "Plataforma Inteligente de Búsqueda y Reunificación Familiar"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "encuentrame-nicaragua-dev-secret-key-32chars-min-prod-change-this!!")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120  # 2 hours for standard session
    
    # Database: Supports SQLite by default for zero-config native execution and PostgreSQL for Docker/prod
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./encuentrame_nicaragua.db"
    )
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "https://creacionvaloria.tradescanner.online",
        "http://creacionvaloria.tradescanner.online",
        "http://encuentramenicaragua:3000",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
    
    # Storage
    STORAGE_DIR: str = os.getenv("STORAGE_DIR", "./storage/uploads")
    MAX_UPLOAD_SIZE_MB: int = 5
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    
    # AI Assistance configuration
    AI_SIMILARITY_THRESHOLD: float = 0.65
    AI_BIOMETRICS_ENABLED: bool = False  # Disabled by design in MVP for human rights compliance

    @model_validator(mode="after")
    def validate_production_security(self):
        if self.ENVIRONMENT.lower() == "production":
            if "change-this" in self.SECRET_KEY or "dev-secret-key" in self.SECRET_KEY:
                raise ValueError(
                    "Configuración de seguridad crítica: En entorno de producción (ENVIRONMENT=production), "
                    "es obligatorio configurar una SECRET_KEY robusta y secreta vía variable de entorno."
                )
        return self

settings = Settings()
