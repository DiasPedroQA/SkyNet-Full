"""Módulo de formatadores e utilitários para o sistema de arquivos"""

from pathlib import Path
from typing import Union


def is_oculto(nome: Union[str, Path]) -> bool:
    """Verifica se um arquivo/pasta é oculto no sistema."""
    return str(nome).strip().startswith(".")


def obter_extensao(caminho: Union[str, Path]) -> str:
    """Obtém a extensão de um arquivo."""
    return Path(str(caminho)).suffix.lower()


def formatar_tamanho(tamanho_bytes: int) -> str:
    """Formata tamanho em bytes para formato legível."""
    if tamanho_bytes < 1024:
        return f"{tamanho_bytes} B"
    if tamanho_bytes < 1024**2:
        return f"{tamanho_bytes / 1024:.1f} KB"
    if tamanho_bytes < 1024**3:
        return f"{tamanho_bytes / 1024**2:.1f} MB"
    return f"{tamanho_bytes / 1024**3:.1f} GB"
