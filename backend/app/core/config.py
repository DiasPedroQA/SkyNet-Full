"""Configurações da aplicação usando Pydantic (valores padrão em dev)."""

from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Classe de configurações carregável via .env automaticamente."""

    app_name: str = "SkyNet-Mobile API"
    debug: bool = True
    allowed_origins_list: List[str] = ["*"]
    database_url: str = "sqlite:///./skynet.db"
    api_v1_prefix: str = "/api/v1"

    class Config:  # pylint: disable=too-few-public-methods
        """Configurações de ambiente da aplicação."""

        env_file = ".env"
        env_file_encoding = "utf-8"


# Instância única de settings utilizada pela aplicação
settings = Settings()
