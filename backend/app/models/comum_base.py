# pylint: disable=too-many-instance-attributes, wrong-import-order, import-error

"""Modelos base para o sistema de arquivos com auto-detecção"""

import mimetypes
import pwd
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, PrivateAttr, field_validator
from services.formatadores import (
    formatar_tamanho,
    identificar_tipo,
    is_oculto,
    obter_extensao,
)

# ============================================================================
# MODELO PRINCIPAL
# ============================================================================


class CaminhoBase(BaseModel):
    """
    Classe base que auto-detecta e carrega propriedades de arquivos/pastas.
    Versão unificada e otimizada com funções auxiliares internas.
    """

    # ========================================================================
    # ATRIBUTOS PÚBLICOS (acessíveis diretamente)
    # ========================================================================
    caminho: str
    nome: str | None = Field(None, description="Nome do arquivo/pasta")
    tipo: str | None = Field(None, description="'arquivo' ou 'pasta'")
    existe: bool = Field(False, description="Se o caminho existe no sistema")

    # Metadados básicos
    tamanho_bytes: int | None = Field(None, description="Tamanho em bytes")
    data_criacao: datetime | None = Field(None, description="Data de criação")
    data_modificacao: datetime | None = Field(None, description="Data da última modificação")
    data_acesso: datetime | None = Field(None, description="Data do último acesso")
    oculto: bool | None = Field(None, description="Se é um arquivo oculto")
    permissoes: str | None = Field(None, description="Permissões em formato octal")
    dono: str | None = Field(None, description="Proprietário do arquivo")
    pai: str | None = Field(None, description="Caminho do diretório pai")
    extensao: str | None = Field(None, description="Extensão do arquivo")
    mime_type: str | None = Field(None, description="Tipo MIME do arquivo")

    # Campos específicos
    linhas: int | None = Field(None, description="Número de linhas (arquivos de texto)")
    itens: list[dict[str, str | int | bool]] = Field(
        default_factory=list, description="Lista de itens da pasta"
    )
    quantidade_itens: int | None = Field(None, description="Quantidade de itens na pasta")
    tamanho_total: int | None = Field(
        None, description="Tamanho total da pasta (soma dos arquivos)"
    )

    # ========================================================================
    # ATRIBUTOS PRIVADOS (apenas para uso interno)
    # ========================================================================
    _erro: str | None = PrivateAttr(default=None)
    _path_obj: Path | None = PrivateAttr(default=None)
    _stat_info: Any | None = PrivateAttr(default=None)  # Any permanece

    # ========================================================================
    # VALIDADORES
    # ========================================================================
    @field_validator("caminho")
    @classmethod
    def validar_caminho(cls, caminho_valor: str) -> str:
        """Valida e normaliza o caminho"""
        if not caminho_valor or not caminho_valor.strip():
            raise ValueError("Caminho não pode ser vazio")

        try:
            caminho_normalizado = Path(caminho_valor).expanduser().resolve()
            return str(caminho_normalizado)
        except (OSError, RuntimeError, ValueError) as e:
            raise ValueError(f"Caminho inválido: {str(e)}") from e

    # ========================================================================
    # INICIALIZAÇÃO
    # ========================================================================
    def __init__(self, **data):
        super().__init__(**data)
        self._carregar_propriedades()

    # ========================================================================
    # PROPRIEDADES COMPUTADAS (para a Classe B acessar de forma controlada)
    # ========================================================================

    @property
    def erro(self) -> str | None:
        """Propriedade de leitura para erro (não pode ser modificada externamente)."""
        return self._erro

    @property
    def info_resumida(self) -> dict[str, Any]:
        """
        Retorna um resumo das informações mais relevantes.
        Ideal para a Classe B consumir.
        """
        base: dict[str, Any] = {
            "caminho": self.caminho,
            "nome": self.nome,
            "tipo": self.tipo,
            "existe": self.existe,
        }

        if self.existe and self.tipo == "arquivo":
            base.update({
                "tamanho": self.tamanho_bytes,
                "tamanho_formatado": self.tamanho_formatado,
                "extensao": self.extensao,
                "mime_type": self.mime_type,
                "linhas": self.linhas,
            })
        elif self.existe and self.tipo == "pasta":
            base.update({
                "itens": len(self.itens),
                "tamanho_total": self.tamanho_total,
                "tamanho_formatado": self.tamanho_formatado,
            })

        return base

    @property
    def info_detalhada(self) -> dict[str, Any]:
        """
        Retorna informações detalhadas (para admin/debug).
        """
        return self.model_dump(exclude_none=True, exclude_unset=True)

    @property
    def tamanho_formatado(self) -> str:
        """Retorna o tamanho formatado (KB, MB, GB)."""
        if self.tamanho_bytes:
            return formatar_tamanho(self.tamanho_bytes)
        return "0 B"

    @property
    def tipo_identificado(self) -> str:
        """Retorna o tipo identificado do arquivo."""
        return identificar_tipo(self.caminho)

    @property
    def is_arquivo(self) -> bool:
        """Verifica se é um arquivo."""
        return self.tipo == "arquivo"

    @property
    def is_pasta(self) -> bool:
        """Verifica se é uma pasta."""
        return self.tipo == "pasta"

    @property
    def path_obj(self) -> Path | None:
        """Retorna o objeto Path (protegido)."""
        return self._path_obj

    # ========================================================================
    # MÉTODOS PÚBLICOS (API para a Classe B)
    # ========================================================================

    def recarregar(self) -> None:
        """Recarrega as propriedades do caminho atual."""
        self._carregar_propriedades()

    def mudar_caminho(self, novo_caminho: str) -> bool:
        """
        Muda para um novo caminho e recarrega propriedades.

        Args:
            novo_caminho: Novo caminho para carregar

        Returns:
            True se o caminho existe e foi carregado, False caso contrário
        """
        try:
            self.caminho = novo_caminho
            self._carregar_propriedades()
            return self.existe
        except (OSError, PermissionError, ValueError):
            return False

    def listar_conteudo_simples(self) -> list[dict[str, Any]]:
        """
        Lista o conteúdo de forma simplificada para a Classe B.
        """
        if not self.is_pasta or not self._path_obj:
            return []

        conteudo = []
        for item in self.itens:
            item_info: dict[str, Any] = {
                "nome": item.get("nome"),
                "tipo": item.get("tipo"),
                "oculto": item.get("oculto", False),
            }

            if item.get("tipo") == "arquivo":
                item_info["tamanho"] = item.get("tamanho")

            conteudo.append(item_info)

        return conteudo

    def buscar_por_nome(self, nome_parcial: str) -> list[dict[str, Any]]:
        """
        Busca itens por nome (case insensitive).
        """
        if not self.is_pasta:
            return []

        resultados = []
        nome_parcial_lower = nome_parcial.lower()

        for item in self.itens:
            nome_item = item.get("nome", "")
            if isinstance(nome_item, str) and nome_parcial_lower in nome_item.lower():
                # Verifica se _path_obj não é None antes de usar
                caminho_base = self._path_obj or Path(self.caminho)
                resultados.append({
                    "nome": nome_item,
                    "tipo": item.get("tipo"),
                    "caminho_completo": str(caminho_base / nome_item),
                })

        return resultados

    # ========================================================================
    # MÉTODOS INTERNOS (protegidos)
    # ========================================================================

    def _carregar_propriedades(self):
        """Carrega todas as propriedades do sistema de arquivos"""
        self._path_obj = Path(self.caminho)
        self._erro = None

        # Verifica existência
        self.existe = self._path_obj.exists()
        if not self.existe:
            self._erro = f"Caminho não existe: {self.caminho}"
            return

        # Propriedades básicas
        self.nome = self._path_obj.name
        self.pai = str(self._path_obj.parent)
        self.oculto = is_oculto(self._path_obj.name)

        # Carrega estatísticas
        self._carregar_estatisticas()

        # Detecta tipo e carrega propriedades específicas
        if self._path_obj.is_file():
            self._carregar_propriedades_arquivo()
        elif self._path_obj.is_dir():
            self._carregar_propriedades_pasta()

    def _carregar_estatisticas(self):
        """Carrega estatísticas básicas do arquivo"""
        if not self._path_obj:
            return

        try:
            self._stat_info = self._path_obj.stat()
            self.data_criacao = datetime.fromtimestamp(self._stat_info.st_ctime)
            self.data_modificacao = datetime.fromtimestamp(self._stat_info.st_mtime)
            self.data_acesso = datetime.fromtimestamp(self._stat_info.st_atime)
            self.permissoes = oct(self._stat_info.st_mode)[-3:]

            # Dono do arquivo
            try:
                self.dono = pwd.getpwuid(self._stat_info.st_uid).pw_name
            except (KeyError, ImportError, OSError):
                self.dono = str(self._stat_info.st_uid)

        except (OSError, PermissionError) as e:
            self._erro = f"Erro ao acessar estatísticas: {str(e)}"

    def _carregar_propriedades_arquivo(self):
        """Carrega propriedades específicas de arquivo"""
        if not self._path_obj or not self._stat_info:
            return

        self.tipo = "arquivo"

        try:
            self.tamanho_bytes = self._stat_info.st_size

            # Extensão
            self.extensao = obter_extensao(caminho=self._path_obj)

            # MIME type
            mime_type, _ = mimetypes.guess_type(str(self._path_obj))
            self.mime_type = mime_type or "application/octet-stream"

            # Conta linhas se for arquivo de texto
            if self.mime_type and self.mime_type.startswith("text/"):
                self._contar_linhas()

        except (OSError, PermissionError) as e:
            self._erro = f"Erro ao processar arquivo: {str(e)}"

    def _carregar_propriedades_pasta(self):
        """Carrega propriedades específicas de pasta"""
        if not self._path_obj:
            return

        self.tipo = "pasta"
        self.tamanho_bytes = 0
        self.itens = []
        self.tamanho_total = 0

        try:
            for item_path in self._path_obj.iterdir():
                item_info = self._get_item_info(item_path)
                self.itens.append(item_info)

                if item_path.is_file():
                    try:
                        self.tamanho_total += item_path.stat().st_size
                    except (OSError, PermissionError):
                        pass

            self.quantidade_itens = len(self.itens)
            self.tamanho_bytes = self.tamanho_total

        except PermissionError:
            self._erro = f"Sem permissão para listar conteúdo de: {self.caminho}"
        except OSError as e:
            self._erro = f"Erro ao acessar pasta: {str(e)}"

    def _get_item_info(self, item_path: Path) -> dict[str, str | int | bool]:
        """Obtém informações básicas de um item da pasta"""
        try:
            stat_info = item_path.stat()
            info: dict[str, str | int | bool] = {
                "nome": item_path.name,
                "tipo": "pasta" if item_path.is_dir() else "arquivo",
                "modificado": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                "oculto": is_oculto(item_path.name),
            }

            if item_path.is_file():
                info["tamanho"] = stat_info.st_size
                info["extensao"] = obter_extensao(item_path)

            return info

        except (OSError, PermissionError):
            return {
                "nome": item_path.name,
                "tipo": "desconhecido",
                "erro": "sem permissão",
            }

    def _contar_linhas(self):
        """Conta o número de linhas em arquivos de texto"""
        if not self._path_obj:
            return

        encodings = ["utf-8", "latin-1", "cp1252"]

        for encoding in encodings:
            try:
                with open(str(self._path_obj), "r", encoding=encoding) as f:
                    self.linhas = sum(1 for _ in f)
                break
            except (UnicodeDecodeError, IOError, PermissionError):
                continue

    # ========================================================================
    # MÉTODOS LEGADO (para compatibilidade)
    # ========================================================================

    def info_completa(self) -> dict[str, Any]:
        """
        Mantido para compatibilidade com código existente.
        """
        return self.info_detalhada
