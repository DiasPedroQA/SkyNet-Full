# pylint: disable=C, R, E, W

"""
CONTROLLER DE SISTEMA
=====================
Camada responsável por rotas HTTP.
Controller NÃO contém regra de negócio.
"""

# from datetime import datetime

from fastapi import APIRouter

# from .config import settings
# from .schemas.system_schema import (
#     SystemInfoSchema,
#     SystemStatsSchema,
# )
# from .schemas.user_schema import (
#     UserCreateSchema,
#     UserResponseSchema,
# )
# from .services.file_service import FileService
# from .services.user_service import UserService

router = APIRouter(prefix="/system", tags=["System"])


# =========================
# Dependency Injection
# =========================


# def get_user_service() -> UserService:
#     return UserService()


# def get_file_service() -> FileService:
#     return FileService()


# =========================
# System Info
# =========================


# @router.get(
#     "/info",
#     response_model=SystemInfoSchema,
#     status_code=status.HTTP_200_OK,
# )
# def get_system_info(
#     user_service: UserService = Depends(get_user_service),
#     file_service: FileService = Depends(get_file_service),
# ) -> SystemInfoSchema:
#     """
#     Retorna informações gerais do sistema.
#     """

#     total_users: int = user_service.count_users()
#     total_files: int = file_service.count_files()

#     stats = SystemStatsSchema(
#         total_users=total_users,
#         total_files=total_files,
#     )

#     return SystemInfoSchema(
#         message="Sistema operacional",
#         docs="/docs",
#         version=settings.APP_VERSION,
#         status="running",
#         system_info=stats,
#         timestamp=datetime.utcnow(),
#     )


# =========================
# User Creation
# =========================


# @router.post(
#     "/users",
#     response_model=UserResponseSchema,
#     status_code=status.HTTP_201_CREATED,
# )
# def create_user(
#     user_data: UserCreateSchema,
#     user_service: UserService = Depends(get_user_service),
# ) -> UserResponseSchema:
#     """
#     Cria um novo usuário no sistema.
#     """

#     user = user_service.create_user(user_data)

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Erro ao criar usuário.",
#         )

#     return UserResponseSchema.model_validate(user)
