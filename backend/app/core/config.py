"""Configurações da aplicação usando Pydantic V2 (valores padrão em dev)."""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Classe de configurações carregável via .env automaticamente.

    Utiliza Pydantic V2 com SettingsConfigDict em vez da classe Config antiga.
    """

    # Configurações da aplicação
    app_name: str = Field(default="SkyNet-Mobile API", description="Nome da aplicação")

    debug: bool = Field(default=True, description="Modo debug (desativar em produção)")

    allowed_origins_list: list[str] = Field(default=["*"], description="Origens permitidas para CORS")

    database_url: str = Field(default="sqlite:///./skynet.db", description="URL de conexão com o banco de dados")

    api_v1_prefix: str = Field(default="/api/v1", description="Prefixo para rotas da API v1")

    # Configurações adicionais para produção
    secret_key: str | None = Field(default=None, description="Chave secreta para JWT (obrigatório em produção)")

    environment: str = Field(default="development", description="Ambiente: development, testing, production")

    # Model config usando a nova sintaxe do Pydantic V2
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignora campos extras no .env
    )

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Valida se o ambiente é um dos valores permitidos."""
        allowed = {"development", "testing", "production"}
        if v not in allowed:
            raise ValueError(f"environment deve ser um de: {allowed}")
        return v

    @field_validator("debug")
    @classmethod
    def validate_debug_mode(cls, v: bool, info) -> bool:
        """Em produção, debug deve ser False."""
        values = info.data
        if values.get("environment") == "production" and v:
            raise ValueError("debug não pode ser True em ambiente de produção")
        return v


# Instância única de settings utilizada pela aplicação
settings = Settings()
