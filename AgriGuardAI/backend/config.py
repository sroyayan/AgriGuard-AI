"""Application configuration for AgriGuard AI."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    app_name: str = os.getenv("AGRIGUARD_APP_NAME", "AgriGuard AI")
    app_env: str = os.getenv("AGRIGUARD_ENV", "production")
    log_level: str = os.getenv("AGRIGUARD_LOG_LEVEL", "INFO")

    model_path: str = os.getenv(
        "AGRIGUARD_MODEL_PATH",
        "models/best.pt",
    )

    model_confidence: float = float(
        os.getenv("AGRIGUARD_MODEL_CONFIDENCE", "0.25")
    )

    max_upload_size_mb: int = int(
        os.getenv("AGRIGUARD_MAX_UPLOAD_SIZE_MB", "10")
    )

    sqlite_path: str = os.getenv(
        "AGRIGUARD_SQLITE_PATH",
        "AgriGuardAI/backend/agriguard.db",
    )

    @property
    def sqlite_absolute_path(self) -> Path:
        """Absolute path to SQLite database."""
        return Path(self.sqlite_path).resolve()


settings = Settings()