"""Modelos de dados para arquivos e pastas do sistema de arquivos"""

from .comum_base import CaminhoBase
from .file_models import ArquivoInfo
from .folder_models import PastaInfo

__all__ = ["CaminhoBase", "ArquivoInfo", "PastaInfo"]
