"""Ponto de entrada da aplicação FastAPI SkyNet-Mobile."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from app.api.v1 import router as v1_router
# settings = {

# }
# # from app.core.database import engine
# # from app.models.favorite import Base

# # ============================================================================
# # Inicialização do Banco de Dados
# # ============================================================================

# # ============================================================================
# # Configuração da Aplicação FastAPI
# # ============================================================================

# app = FastAPI(
#     title=settings.app_name,
#     description="API para gerenciamento de favoritos do SkyNet-Mobile",
#     version="0.1.0",
#     debug=settings.debug,
#     docs_url="/docs" if settings.debug else None,  # Só mostra docs em dev
#     redoc_url="/redoc" if settings.debug else None,  # Só mostra redoc em dev
# )


# # ============================================================================
# # Middleware CORS
# # ============================================================================

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.allowed_origins_list,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # ============================================================================
# # Rotas da API
# # ============================================================================

# # Inclui todas as rotas da versão 1 da API
# app.include_router(v1_router)


# # ============================================================================
# # Endpoints de Saúde e Informações
# # ============================================================================


# @app.get("/")
# async def root() -> dict:
#     """
#     Endpoint raiz com informações básicas da API.

#     Returns:
#         Dict com mensagem de boas-vindas e informações da API
#     """
#     return {
#         "message": "🚀 Bem-vindo à SkyNet-Mobile API!",
#         "app": settings.app_name,
#         "version": "0.1.0",
#         "docs": "/docs" if settings.debug else "Disponível apenas em desenvolvimento",
#         "health": "/health",
#     }


# @app.get("/health")
# async def health_check() -> dict:
#     """
#     Endpoint para verificar a saúde da API.

#     Returns:
#         Dict com status da aplicação e configurações básicas
#     """
#     return {
#         "status": "healthy",
#         "app": settings.app_name,
#         "debug": settings.debug,
#         "database": "sqlite" if "sqlite" in settings.database_url else "postgresql",
#     }


# @app.get("/info")
# async def info() -> dict:
#     """
#     Endpoint com informações detalhadas da API.

#     Returns:
#         Dict com configurações não sensíveis da aplicação
#     """
#     return {
#         "app_name": settings.app_name,
#         "version": "0.1.0",
#         "debug": settings.debug,
#         "api_prefix": settings.api_v1_prefix,
#         "cors_origins": settings.allowed_origins_list,
#         "environment": "development" if settings.debug else "production",
#     }


# # ============================================================================
# # Execução direta (apenas para desenvolvimento)
# # ============================================================================

# if __name__ == "__main__":
#     import uvicorn

#     print(f"🚀 Iniciando {settings.app_name}...")
#     print("📝 Documentação disponível em http://localhost:8000/docs")
#     print(f"🔍 Modo debug: {settings.debug}")

#     uvicorn.run(
#         "app.main:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=settings.debug,  # Auto-reload apenas em desenvolvimento
#         log_level="debug" if settings.debug else "info",
#     )
