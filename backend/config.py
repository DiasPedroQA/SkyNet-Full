# backend/config.py

"""
Configuração central da aplicação.

Responsável por:
- Carregar variáveis do .env
- Converter tipos
- Definir valores padrão seguros
- Expor propriedades utilitárias
"""

import json
import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

# =============================================================================
# Carregamento do .env (determinístico)
# =============================================================================

BASE_DIR: Path = Path(__file__).resolve().parent.parent
ENV_FILE: Path = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# =============================================================================
# Settings
# =============================================================================


class Settings:
    """
    Configurações da aplicação carregadas do ambiente.
    """

    def __init__(self) -> None:

        # ---------------------------------------------------------------------
        # Aplicação
        # ---------------------------------------------------------------------
        self.app_name: str = os.getenv("APP_NAME", "File Manager API")
        self.app_version: str = os.getenv("APP_VERSION", "1.0.0")
        self.environment: str = os.getenv("ENVIRONMENT", "development")

        # ---------------------------------------------------------------------
        # Servidor
        # ---------------------------------------------------------------------
        self.api_host: str = os.getenv("API_HOST", "0.0.0.0")
        self.api_port: int = int(os.getenv("API_PORT", "8000"))
        self.api_debug: bool = os.getenv("API_DEBUG", "false").lower() == "true"

        # ---------------------------------------------------------------------
        # Banco de Dados
        # ---------------------------------------------------------------------
        self.database_url: str = os.getenv(
            "DATABASE_URL",
            "sqlite:///./backend/database.db",
        )

        # ---------------------------------------------------------------------
        # Upload
        # ---------------------------------------------------------------------
        self.upload_dir: Path = Path(os.getenv("UPLOAD_DIR", "./uploads"))
        self.max_upload_size: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))

        self.allowed_extensions: list[str] = self._parse_extensions()

        # ---------------------------------------------------------------------
        # Logging
        # ---------------------------------------------------------------------
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        log_file: str | None = os.getenv("LOG_FILE")
        self.log_file: Path | None = Path(log_file) if log_file else None

    # =========================================================================
    # Métodos auxiliares
    # =========================================================================

    @staticmethod
    def _parse_extensions() -> list[str]:
        raw: str = os.getenv(
            "ALLOWED_EXTENSIONS",
            '[".jpg", ".png", ".pdf"]',
        )
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return [".jpg", ".png", ".pdf"]

    # =========================================================================
    # Propriedades úteis
    # =========================================================================

    @property
    def is_development(self) -> bool:
        """Retorna True se o ambiente for desenvolvimento."""
        return self.environment.lower() == "development"


# =============================================================================
# Instância Singleton
# =============================================================================


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna uma instância cacheada das configurações.
    """
    return Settings()


settings: Settings = get_settings()
