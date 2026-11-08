import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings:
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "none")
    LLM_TIMEOUT_SECONDS: float = float(os.getenv("LLM_TIMEOUT_SECONDS", "4.0"))
    DEMO_TODAY: str = os.getenv("DEMO_TODAY", "2026-07-15")
    OTP_DEMO_CODE: str = os.getenv("OTP_DEMO_CODE", "123456")
    UPLOAD_TTL_MINUTES: int = int(os.getenv("UPLOAD_TTL_MINUTES", "30"))
    CORS_ORIGIN: str = os.getenv("CORS_ORIGIN", "http://localhost:5173")
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'app.db'}")
    DATA_DIR: Path = BASE_DIR / "data"
    UPLOAD_DIR: Path = BASE_DIR / "tmp_uploads"

settings = Settings()
