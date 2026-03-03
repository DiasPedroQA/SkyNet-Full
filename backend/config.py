# backend/config.py

"""
Configuração central da aplicação usando Pydantic Settings (v2).

Responsável por:
- Carregar variáveis automaticamente do .env
- Converter tipos automaticamente
- Validar valores
- Fornecer defaults seguros
- Expor propriedades utilitárias
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações globais da aplicação.

    Os valores são carregados automaticamente do arquivo `.env`
    ou das variáveis de ambiente do sistema.
    """

    # =========================================================================
    # Aplicação
    # =========================================================================

    app_name: str = Field(default="SkyNet-Mobile API")
    app_version: str = Field(default="1.0.0")
    environment: Literal["development", "testing", "production"] = "development"

    # =========================================================================
    # Servidor
    # =========================================================================

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = False

    # =========================================================================
    # Banco de Dados
    # =========================================================================

    database_url: str = "sqlite:///./backend/database.db"

    # =========================================================================
    # Upload
    # =========================================================================

    upload_dir: Path = Path("./uploads")
    max_upload_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: list[str] = [".jpg", ".png", ".pdf"]

    # =========================================================================
    # Logging
    # =========================================================================

    log_level: str = "INFO"
    log_file: Path | None = None

    # =========================================================================
    # Configuração do Pydantic Settings
    # =========================================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # =========================================================================
    # Validações
    # =========================================================================

    @field_validator("api_debug")
    @classmethod
    def validate_debug_in_production(cls, value: bool, info) -> bool:
        """
        Garante que debug não esteja ativado em produção.
        """
        if info.data.get("environment") == "production" and value:
            raise ValueError("api_debug não pode ser True em produção")
        return value

    # =========================================================================
    # Propriedades úteis
    # =========================================================================

    @property
    def is_development(self) -> bool:
        """Retorna True se o ambiente for development."""
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        """Retorna True se o ambiente for production."""
        return self.environment == "production"


# =============================================================================
# Instância Singleton (cacheada)
# =============================================================================


@lru_cache
def get_settings() -> Settings:
    """
    Retorna instância única e cacheada de Settings.

    Evita recriação desnecessária e mantém padrão singleton.
    """
    return Settings()


settings: Settings = get_settings()
