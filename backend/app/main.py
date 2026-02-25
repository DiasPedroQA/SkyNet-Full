"""Ponto de entrada da aplicação FastAPI SkyNet-Mobile."""

import uvicorn

# Carrega configurações centralizadas
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.interfaces.api.v1 import router as V1_ROUTER

# Importa router v1 de forma segura (se o pacote estiver incompleto evita crash)
try:
    _HAS_V1_ROUTER = True
except (ImportError, ModuleNotFoundError):
    V1_ROUTER = None
    _HAS_V1_ROUTER = False

# ============================================================================
# Configuração da aplicação FastAPI
# ============================================================================
app: FastAPI = FastAPI(
    title=settings.app_name,
    description="API para gerenciamento de favoritos do SkyNet-Mobile",
    version="0.1.0",
    debug=settings.debug,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# ============================================================================
# Middleware CORS (origens configuráveis via settings)
# ============================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Rotas da API
# ============================================================================
# Inclui router v1 apenas se estiver disponível (evita falhas em dev)
if _HAS_V1_ROUTER and V1_ROUTER is not None:
    app.include_router(V1_ROUTER, prefix=settings.api_v1_prefix)


# ============================================================================
# Endpoints de Saúde e Informações (simples e úteis para checks)
# ============================================================================
@app.get("/")
async def root() -> dict[str, str | bool | int]:
    """Endpoint raiz para verificar se a API está rodando."""
    return {
        "message": "🚀 Bem-vindo à SkyNet-Mobile API!",
        "app": settings.app_name,
        "version": "0.1.0",
        "docs": "/docs" if settings.debug else "Disponível apenas em desenvolvimento",
        "health": "/health",
    }


@app.get("/health")
async def health_check() -> dict[str, str | bool]:
    """Endpoint para verificar a saúde da aplicação."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "debug": settings.debug,
        "database": "sqlite" if "sqlite" in settings.database_url else "postgresql",
    }


@app.get("/info")
async def info() -> dict[str, str | bool | list[str]]:
    """Endpoint para retornar informações básicas da aplicação."""
    return {
        "app_name": settings.app_name,
        "version": "0.1.0",
        "debug": settings.debug,
        "api_prefix": settings.api_v1_prefix,
        "cors_origins": settings.allowed_origins_list,
        "environment": "development" if settings.debug else "production",
    }


# Execução direta: apenas para desenvolvimento local
if __name__ == "__main__":
    print(f"🚀 Iniciando {settings.app_name}...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info",
    )
