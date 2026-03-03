# """Modelos base para o sistema de arquivos com auto-detecção"""

# import contextlib
# import mimetypes
# import pwd
# from datetime import datetime
# from pathlib import Path
# from typing import Any

# from pydantic import BaseModel, Field, PrivateAttr, field_validator

# from app.infrastructure.services.formatadores import is_oculto, obter_extensao


# class CaminhoBase(BaseModel):
#     """
#     Classe base que representa um caminho no sistema de arquivos.
#     Trata de forma neutra, sem assumir se é arquivo ou pasta.
#     """

#     caminho: str = Field(..., description="Caminho absoluto do arquivo ou pasta")
#     nome: str | None = Field(None, description="Nome do arquivo/pasta")
#     tipo: str | None = Field(None, description="'arquivo' ou 'pasta'")
#     existe: bool = Field(False, description="Se o caminho existe no sistema")

#     # Propriedades comuns
#     tamanho_bytes: int | None = Field(None, description="Tamanho em bytes")
#     data_criacao: datetime | None = Field(None, description="Data de criação")
#     data_modificacao: datetime | None = Field(None, description="Data da última modificação")
#     data_acesso: datetime | None = Field(None, description="Data do último acesso")
#     oculto: bool | None = Field(None, description="Se é um arquivo oculto")
#     permissoes: str | None = Field(None, description="Permissões em formato octal")
#     dono: str | None = Field(None, description="Proprietário do arquivo")
#     pai: str | None = Field(None, description="Caminho do diretório pai")
#     extensao: str | None = Field(None, description="Extensão do arquivo")
#     mime_type: str | None = Field(None, description="Tipo MIME do arquivo")

#     # Propriedades específicas
#     linhas: int | None = Field(None, description="Número de linhas (arquivos de texto)")
#     itens: list = Field(default_factory=list, description="Lista de itens da pasta")
#     quantidade_itens: int | None = Field(None, description="Quantidade de itens na pasta")
#     tamanho_total: int | None = Field(None, description="Tamanho total da pasta (soma dos arquivos)")

#     _erro: str | None = PrivateAttr(default=None)
#     _objeto_caminho: Path | None = PrivateAttr(default=None)
#     _info_estatisticas = PrivateAttr(default=None)

#     @field_validator("caminho", mode="before")
#     @classmethod
#     def _validar_caminho(cls, v: str | Path) -> str:
#         """Aceita Path ou str e normaliza para string absoluta."""
#         if isinstance(v, Path):
#             v = str(v)
#         if not v or not str(v).strip():
#             raise ValueError("Caminho não pode ser vazio")
#         try:
#             return str(Path(v).expanduser().resolve(strict=False))
#         except (OSError, ValueError, RuntimeError):
#             return str(Path(v))

#     def __init__(self, **data: Any) -> None:
#         super().__init__(**data)
#         self._carregar_caminho()

#     # =========================================================================
#     # PROPRIEDADES
#     # =========================================================================

#     @property
#     def is_pasta(self) -> bool:
#         """Verifica se o caminho é uma pasta."""
#         return self.tipo == "pasta"

#     @property
#     def info_detalhada(
#         self,
#     ) -> dict[str, str | bool | int | datetime | list[dict[str, str | int | bool | None]] | None]:
#         """Retorna dict com todas as informações relevantes."""
#         return {
#             "caminho": self.caminho,
#             "nome": self.nome,
#             "tipo": self.tipo,
#             "existe": self.existe,
#             "tamanho_bytes": self.tamanho_bytes,
#             "tamanho_total": self.tamanho_total,
#             "linhas": self.linhas,
#             "data_criacao": self.data_criacao,
#             "data_modificacao": self.data_modificacao,
#             "data_acesso": self.data_acesso,
#             "oculto": self.oculto,
#             "permissoes": self.permissoes,
#             "dono": self.dono,
#             "pai": self.pai,
#             "extensao": self.extensao,
#             "mime_type": self.mime_type,
#             "itens": self.itens,
#             "quantidade_itens": self.quantidade_itens,
#             "erro": self._erro,
#         }

#     # =========================================================================
#     # MÉTODOS PRINCIPAIS
#     # =========================================================================

#     def _carregar_caminho(self) -> None:
#         """Carrega todas as propriedades do caminho."""
#         self._objeto_caminho = Path(self.caminho)
#         self._erro = None
#         self.existe = self._objeto_caminho.exists()

#         if not self.existe:
#             self._definir_valores_padrao()
#             return

#         self._carregar_propriedades_basicas()
#         self._carregar_estatisticas()
#         self._carregar_propriedades_especificas()

#     def _definir_valores_padrao(self) -> None:
#         """Define valores padrão para caminho inexistente."""
#         self.tipo = None
#         self.tamanho_bytes = 0
#         self.data_criacao = None
#         self.data_modificacao = None
#         self.data_acesso = None
#         self._erro = f"Caminho não existe: {self.caminho}"

#     def _carregar_propriedades_basicas(self) -> None:
#         """Carrega propriedades básicas do caminho."""
#         if not self._objeto_caminho:
#             return
#         self.nome = self._objeto_caminho.name
#         self.pai = str(self._objeto_caminho.parent)
#         self.oculto = is_oculto(self._objeto_caminho.name)

#     def _carregar_propriedades_especificas(self) -> None:
#         """Delega para método específico baseado no tipo."""
#         if not self._objeto_caminho:
#             return

#         if self._objeto_caminho.is_file():
#             self._carregar_como_arquivo()
#         elif self._objeto_caminho.is_dir():
#             self._carregar_como_pasta()

#     # =========================================================================
#     # ESTATÍSTICAS
#     # =========================================================================

#     def _carregar_estatisticas(self) -> None:
#         """Carrega estatísticas básicas do caminho."""
#         if not self._objeto_caminho:
#             return

#         try:
#             self._info_estatisticas = self._objeto_caminho.stat()
#             self.data_criacao = datetime.fromtimestamp(self._info_estatisticas.st_ctime)
#             self.data_modificacao = datetime.fromtimestamp(self._info_estatisticas.st_mtime)
#             self.data_acesso = datetime.fromtimestamp(self._info_estatisticas.st_atime)
#             self.permissoes = oct(self._info_estatisticas.st_mode)[-3:]
#             self._carregar_dono()

#         except (OSError, PermissionError) as e:
#             self._erro = f"Erro ao acessar estatísticas: {str(e)}"

#     def _carregar_dono(self) -> None:
#         """Carrega informação do dono do arquivo."""
#         if not self._info_estatisticas:
#             return
#         try:
#             self.dono = pwd.getpwuid(self._info_estatisticas.st_uid).pw_name
#         except (KeyError, ImportError, OSError):
#             self.dono = str(self._info_estatisticas.st_uid)

#     # =========================================================================
#     # CARREGAMENTO POR TIPO
#     # =========================================================================

#     def _carregar_como_arquivo(self) -> None:
#         """Carrega propriedades específicas de arquivo."""
#         self.tipo = "arquivo"

#         if not self._info_estatisticas:
#             return

#         try:
#             self.tamanho_bytes = self._info_estatisticas.st_size
#             if self._objeto_caminho is not None:
#                 self.extensao = obter_extensao(caminho=self._objeto_caminho)
#                 self._carregar_mime_type()
#                 self._tentar_contar_linhas()

#         except (OSError, PermissionError) as e:
#             self._erro = f"Erro ao processar arquivo: {str(e)}"

#     def _carregar_como_pasta(self) -> None:
#         """Carrega propriedades específicas de pasta."""
#         self.tipo = "pasta"
#         self.tamanho_bytes = 0
#         self.itens = []
#         self.tamanho_total = 0

#         if self._objeto_caminho is None:
#             return

#         try:
#             for item_path in self._objeto_caminho.iterdir():
#                 item_info = self._criar_info_item(item_path)
#                 self.itens.append(item_info)
#                 self._acumular_tamanho_item(item_path)

#             self.quantidade_itens = len(self.itens)
#             if self.tamanho_total is not None:
#                 self.tamanho_bytes = self.tamanho_total

#         except PermissionError:
#             self._erro = f"Sem permissão para listar: {self.caminho}"
#         except OSError as e:
#             self._erro = f"Erro ao acessar pasta: {str(e)}"

#     # =========================================================================
#     # MÉTODOS AUXILIARES
#     # =========================================================================

#     def _carregar_mime_type(self) -> None:
#         """Carrega o tipo MIME do arquivo."""
#         if not self._objeto_caminho:
#             return
#         mime_type, _ = mimetypes.guess_type(str(self._objeto_caminho))
#         self.mime_type = mime_type or "application/octet-stream"

#     def _tentar_contar_linhas(self) -> None:
#         """Tenta contar linhas se for arquivo de texto."""
#         if self.mime_type and self.mime_type.startswith("text/") and self._objeto_caminho is not None:
#             self._contar_linhas()

#     def _contar_linhas(self) -> None:
#         """Conta o número de linhas em arquivos de texto."""
#         if self._objeto_caminho is None:
#             return

#         encodings = ["utf-8", "latin-1", "cp1252"]

#         for encoding in encodings:
#             try:
#                 with open(str(self._objeto_caminho), "r", encoding=encoding) as f:
#                     self.linhas = sum(1 for _ in f)
#                 break
#             except (UnicodeDecodeError, IOError, PermissionError):
#                 continue

#     def _criar_info_item(self, item_path: Path) -> dict:
#         """Cria dicionário com informações de um item."""
#         try:
#             stat_info = item_path.stat()
#             info: dict = {
#                 "nome": item_path.name,
#                 "tipo": "pasta" if item_path.is_dir() else "arquivo",
#                 "modificado": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
#                 "oculto": is_oculto(item_path.name),
#             }

#             if item_path.is_file():
#                 info["tamanho"] = stat_info.st_size
#                 info["extensao"] = obter_extensao(item_path)

#             return info

#         except (OSError, PermissionError):
#             return {
#                 "nome": item_path.name,
#                 "tipo": "desconhecido",
#                 "erro": "sem permissão",
#             }

#     def _acumular_tamanho_item(self, item_path: Path) -> None:
#         """Acumula tamanho do item ao total da pasta."""
#         if item_path.is_file():
#             with contextlib.suppress(OSError, PermissionError):
#                 tamanho = item_path.stat().st_size
#                 if self.tamanho_total is None:
#                     self.tamanho_total = tamanho
#                 else:
#                     self.tamanho_total += tamanho

#     # =========================================================================
#     # MÉTODO LEGADO
#     # =========================================================================

#     def info_completa(self) -> dict[str, str | bool | int | datetime | list[dict[str, str | int | bool | None]] | None]:
#         """Fornece dicionário completo (compatibilidade com código anterior)."""
#         return self.info_detalhada
