# pylint: disable=C, R, E, W

"""Módulo de serviços do sistema"""

# import os
# from datetime import datetime
# from pathlib import Path

# from models.system_info_model import FileModel
# from repositories.user_repository import FileRepository

# from .config import settings
# from .schemas.system_schema import (
#     SystemInfoSchema,
#     SystemStatsSchema,
# )
# from .services.user_service import UserService


# class FileService:
#     """Responsável pela regra de negócio relacionada a arquivos."""

#     def __init__(self, upload_dir: str = "uploads") -> None:
#         self.repository = FileRepository()
#         self.upload_dir = Path(upload_dir)
#         self.upload_dir.mkdir(parents=True, exist_ok=True)

#     def save_file(
#         self,
#         file_content: bytes,
#         filename: str,
#         user_id: int,
#     ) -> FileModel:
#         """Salva um arquivo no sistema, garantindo um caminho único."""
#         file_path: Path = self._generate_unique_path(filename, user_id)

#         file_path.write_bytes(file_content)

#         file_model = FileModel(
#             name=file_path.name,
#             path=str(file_path),
#             size=file_path.stat().st_size,
#             user_id=user_id,
#         )

#         return self.repository.create(file_model)

#     def get_user_files(self, user_id: int) -> list[FileModel]:
#         """Lista os arquivos de um usuário específico."""
#         return self.repository.find_by_user(user_id)

#     def delete_file(self, file_id: int, user_id: int) -> None:
#         """Deleta um arquivo verificando se pertence ao usuário."""

#         file: FileModel | None = self.repository.find_by_id(file_id)

#         if file is None:
#             raise ValueError("Arquivo não encontrado")

#         if file.user_id != user_id:
#             raise PermissionError("Usuário não autorizado")

#         Path(file.path).unlink(missing_ok=True)

#         self.repository.delete(file_id)

#     def _generate_unique_path(self, filename: str, user_id: int) -> Path:
#         """Gera um caminho único para o arquivo, evitando sobrescritas."""
#         base_path: Path = self.upload_dir / f"{user_id}_{filename}"
#         file_path: Path = base_path
#         counter = 1

#         while file_path.exists():
#             name, ext = os.path.splitext(filename)
#             file_path = self.upload_dir / f"{user_id}_{name}_{counter}{ext}"
#             counter += 1

#         return file_path


# class SystemService:
#     def __init__(self) -> None:
#         self.user_service = UserService()
#         self.file_service = FileService()

#     def get_system_info(self) -> SystemInfoSchema:

#         total_users = self.user_service.count_users()
#         total_files = self.file_service.count_files()

#         stats = SystemStatsSchema(
#             total_users=total_users,
#             total_files=total_files,
#         )

#         return SystemInfoSchema(
#             message="Sistema operacional",
#             version=settings.APP_VERSION,
#             status="running",
#             system_info=stats,
#             timestamp=datetime.now(),
#         )
