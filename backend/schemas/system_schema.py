# pylint: disable=C, R, E, W
"""
SCHEMAS DA APLICAÇÃO
====================
Define os schemas Pydantic para validação de dados de entrada e saída da API.
"""

from datetime import datetime
# from typing import Optional

from pydantic import BaseModel, ConfigDict

# =============================================================================
# SCHEMAS DO SISTEMA
# =============================================================================


class SystemStatsSchema(BaseModel):
    total_users: int
    total_files: int


class SystemInfoSchema(BaseModel):
    message: str
    docs: str
    version: str
    status: str
    system_info: SystemStatsSchema
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# SCHEMAS DE ARQUIVOS
# =============================================================================


# class FileUploadSchema(BaseModel):
#     """
#     Schema para validação de upload de arquivo.

#     Attributes:
#         name: Nome do arquivo (max 255 caracteres)
#         description: Descrição opcional do arquivo
#         is_public: Se o arquivo é público ou privado
#     """

#     name: str = Field(
#         ..., max_length=255, description="Nome do arquivo (máximo 255 caracteres)"
#     )
#     description: Optional[str] = Field(
#         None, max_length=500, description="Descrição opcional do arquivo"
#     )
#     is_public: bool = Field(
#         False, description="True se o arquivo for público, False se privado"
#     )

#     @field_validator("name")
#     @classmethod
#     def validate_filename(cls, v: str) -> str:
#         """
#         Valida se o nome do arquivo não contém caracteres perigosos.
#         """
#         v = v.strip()

#         if not v:
#             raise ValueError("Nome do arquivo não pode estar vazio")

#         dangerous_chars = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]
#         if any(char in v for char in dangerous_chars):
#             raise ValueError(
#                 f"Nome do arquivo não pode conter caracteres especiais: {dangerous_chars}"
#             )

#         return v

#     model_config = ConfigDict(
#         json_schema_extra={
#             "example": {
#                 "name": "documento.pdf",
#                 "description": "Documento importante",
#                 "is_public": True,
#             }
#         }
#     )


# class FileResponseSchema(BaseModel):
#     """
#     Schema para resposta com dados do arquivo.
#     """

#     id: int = Field(..., description="ID único do arquivo")
#     name: str = Field(..., description="Nome do arquivo")
#     path: str = Field(..., description="Caminho relativo do arquivo")
#     size: int = Field(..., description="Tamanho em bytes", ge=0)
#     size_formatted: str = Field(..., description="Tamanho formatado para exibição")
#     user_id: int = Field(..., description="ID do usuário proprietário")
#     created_at: str = Field(..., description="Data de criação (ISO 8601)")

#     model_config = ConfigDict(
#         from_attributes=True,
#         json_schema_extra={
#             "example": {
#                 "id": 1,
#                 "name": "documento.pdf",
#                 "path": "/uploads/1/documento.pdf",
#                 "size": 1048576,
#                 "size_formatted": "1.0 MB",
#                 "user_id": 1,
#                 "created_at": "2024-01-01T10:30:00Z",
#             }
#         },
#     )


# =============================================================================
# SCHEMAS DE USUÁRIO
# =============================================================================


# class UserBaseSchema(BaseModel):
#     """
#     Schema base para usuários com campos comuns.
#     """

#     username: str = Field(
#         ...,
#         min_length=3,
#         max_length=50,
#         description="Nome de usuário (3-50 caracteres)",
#     )
#     email: EmailStr = Field(..., description="Email válido do usuário")

#     @field_validator("username")
#     @classmethod
#     def validate_username(cls, v: str) -> str:
#         """
#         Valida o formato do username.
#         """
#         v = v.strip().lower()

#         if len(v) < 3:
#             raise ValueError("Username deve ter pelo menos 3 caracteres")

#         if len(v) > 50:
#             raise ValueError("Username deve ter no máximo 50 caracteres")

#         if not v.replace("_", "").isalnum():
#             raise ValueError(
#                 "Username deve conter apenas letras, números e underscore (_)"
#             )

#         return v


# class UserCreateSchema(UserBaseSchema):
#     """
#     Schema para criação de novo usuário.
#     """

#     password: str = Field(
#         ...,
#         min_length=6,
#         max_length=100,
#         description="Senha do usuário (mínimo 6 caracteres)",
#     )

#     @field_validator("password")
#     @classmethod
#     def validate_password(cls, v: str) -> str:
#         """
#         Valida a força da senha.
#         """
#         if len(v) < 6:
#             raise ValueError("Senha deve ter pelo menos 6 caracteres")

#         if not any(char.isdigit() for char in v):
#             raise ValueError("Senha deve conter pelo menos um número")

#         if not any(char.isupper() for char in v):
#             raise ValueError("Senha deve conter pelo menos uma letra maiúscula")

#         return v

#     model_config = ConfigDict(
#         json_schema_extra={
#             "example": {
#                 "username": "joao_silva",
#                 "email": "joao@email.com",
#                 "password": "Senha123",
#             }
#         }
#     )


# class UserLoginSchema(BaseModel):
#     """
#     Schema para login de usuário.
#     """

#     email: EmailStr = Field(..., description="Email do usuário")
#     password: str = Field(..., description="Senha do usuário")

#     model_config = ConfigDict(
#         json_schema_extra={
#             "example": {"email": "joao@email.com", "password": "Senha123"}
#         }
#     )


# class UserResponseSchema(UserBaseSchema):
#     """
#     Schema para resposta com dados do usuário (sem senha).
#     """

#     id: int = Field(..., description="ID único do usuário")
#     created_at: str = Field(..., description="Data de criação")
#     is_active: bool = Field(True, description="Se a conta está ativa")
#     is_admin: bool = Field(False, description="Se é administrador")

#     @field_validator("created_at")
#     @classmethod
#     def validate_datetime(cls, v: str) -> str:
#         """
#         Valida se a string de data está no formato ISO.
#         """
#         try:
#             datetime.fromisoformat(v.replace("Z", "+00:00"))
#         except (ValueError, TypeError):
#             raise ValueError("Data deve estar no formato ISO 8601")
#         return v

#     model_config = ConfigDict(
#         from_attributes=True,
#         json_schema_extra={
#             "example": {
#                 "id": 1,
#                 "username": "joao_silva",
#                 "email": "joao@email.com",
#                 "created_at": "2024-01-01T10:00:00Z",
#                 "is_active": True,
#                 "is_admin": False,
#             }
#         },
#     )


# class UserUpdateSchema(BaseModel):
#     """
#     Schema para atualização de usuário (todos campos opcionais).
#     """

#     username: Optional[str] = Field(
#         None, min_length=3, max_length=50, description="Novo nome de usuário"
#     )
#     email: Optional[EmailStr] = Field(None, description="Novo email")
#     password: Optional[str] = Field(
#         None, min_length=6, max_length=100, description="Nova senha"
#     )
#     is_active: Optional[bool] = Field(None, description="Ativar/desativar conta")
#     is_admin: Optional[bool] = Field(None, description="Definir como admin")

#     @field_validator("username")
#     @classmethod
#     def validate_username(cls, v: Optional[str]) -> Optional[str]:
#         """Valida username se fornecido"""
#         if v is None:
#             return v
#         return UserBaseSchema.validate_username(v)

#     @field_validator("password")
#     @classmethod
#     def validate_password(cls, v: Optional[str]) -> Optional[str]:
#         """Valida senha se fornecida"""
#         if v is None:
#             return v
#         return UserCreateSchema.validate_password(v)

#     model_config = ConfigDict(
#         json_schema_extra={
#             "example": {"username": "joao_novo", "email": "joao.novo@email.com"}
#         }
#     )
