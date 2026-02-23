"""Módulo de formatadores e utilitários para o sistema de arquivos"""

from pathlib import Path
from typing import Any, Union

# ============================================================================
# CONSTANTES
# ============================================================================

# Extensões organizadas por categoria (já existentes)
EXTENSOES_PDF = {".pdf"}
EXTENSOES_IMAGEM = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"}
EXTENSOES_TEXTO = {
    ".txt",
    ".md",
    ".csv",
    ".json",
    ".xml",
    ".html",
    ".css",
    ".js",
    ".py",
    ".yml",
    ".yaml",
    ".ini",
    ".cfg",
    ".conf",
    ".log",
}
EXTENSOES_EXECUTAVEIS = {".sh", ".bash", ".exe", ".bat", ".cmd", ".ps1"}

# Mapeamento de tipos (já existente)
TIPOS_ARQUIVO = {
    # ... (mantém o mesmo do arquivo anterior)
    ".txt": "texto",
    ".md": "markdown",
    ".pdf": "documento",
    # ... (todo o mapeamento existente)
}


# ============================================================================
# FUNÇÕES DE VERIFICAÇÃO DE EXTENSÃO (já existentes)
# ============================================================================


def verificar_extensao(extensao: str, *extensoes_permitidas: str) -> bool:
    """Verifica se uma extensão está na lista de extensões permitidas."""
    if not extensao:
        return False
    extensao_atual = extensao.lower()
    return any(extensao_atual == ext.lower() for ext in extensoes_permitidas)


def verificar_extensao_por_categoria(extensao: str, categorias: set) -> bool:
    """Verifica se uma extensão pertence a uma categoria."""
    return extensao.lower() in categorias


def eh_pdf(extensao: str) -> bool:
    """Verifica se a extensão é de PDF."""
    return verificar_extensao_por_categoria(extensao, EXTENSOES_PDF)


def eh_imagem(extensao: str) -> bool:
    """Verifica se a extensão é de imagem."""
    return verificar_extensao_por_categoria(extensao, EXTENSOES_IMAGEM)


def eh_texto(extensao: str) -> bool:
    """Verifica se a extensão é de arquivo de texto."""
    return verificar_extensao_por_categoria(extensao, EXTENSOES_TEXTO)


def eh_executavel(extensao: str, permissoes: str = "") -> bool:
    """Verifica se o arquivo é executável (por extensão ou permissões)."""
    if extensao and extensao.lower() in EXTENSOES_EXECUTAVEIS:
        return True

    if permissoes and len(permissoes) == 3:
        return int(permissoes[-1]) % 2 == 1

    return False


# ============================================================================
# FUNÇÕES AUXILIARES DE SISTEMA DE ARQUIVOS (já existentes)
# ============================================================================


def is_oculto(nome: str) -> bool:
    """Verifica se um arquivo/pasta é oculto no sistema."""
    return nome.startswith(".")


def obter_extensao(caminho: Union[str, Path]) -> str:
    """Obtém a extensão de um arquivo."""
    if isinstance(caminho, str):
        caminho = Path(caminho)
    return caminho.suffix.lower()


def formatar_tamanho(tamanho_bytes: int) -> str:
    """Formata tamanho em bytes para formato legível."""
    if tamanho_bytes < 1024:
        return f"{tamanho_bytes} B"
    elif tamanho_bytes < 1024**2:
        return f"{tamanho_bytes / 1024:.1f} KB"
    elif tamanho_bytes < 1024**3:
        return f"{tamanho_bytes / 1024**2:.1f} MB"
    else:
        return f"{tamanho_bytes / 1024**3:.1f} GB"


def identificar_tipo(caminho: Union[str, Path]) -> str:
    """Identifica o tipo genérico de um arquivo."""
    extensao = Path(caminho).suffix.lower() if isinstance(caminho, str) else caminho.suffix.lower()
    return TIPOS_ARQUIVO.get(extensao, "desconhecido")


# ============================================================================
# NOVAS FUNÇÕES ESPECÍFICAS PARA PASTAS
# ============================================================================


def formatar_info_item_pasta(
    nome: str,
    tipo: str,
    oculto: bool,
    tamanho: int | None = None,
    tamanho_formatado: str | None = None,
    extensao: str | None = None,
    modificado: str | None = None,
) -> dict[str, Any]:
    """
    Formata informações de um item dentro de uma pasta.

    Args:
        nome: Nome do item
        tipo: 'arquivo' ou 'pasta'
        oculto: Se é oculto
        tamanho: Tamanho em bytes (para arquivos)
        tamanho_formatado: Tamanho formatado (para arquivos)
        extensao: Extensão (para arquivos)
        modificado: Data de modificação

    Returns:
        Dicionário com informações formatadas do item
    """
    info = {
        "nome": nome,
        "tipo": tipo,
        "oculto": oculto,
    }

    if tipo == "arquivo":
        if tamanho is not None:
            info["tamanho"] = tamanho
        if tamanho_formatado is not None:
            info["tamanho_formatado"] = tamanho_formatado
        if extensao is not None:
            info["extensao"] = extensao
        if modificado is not None:
            info["modificado"] = modificado

    return info


def contar_itens_por_tipo(itens: list[dict[str, Any]]) -> dict[str, int]:
    """
    Conta itens por tipo em uma lista.

    Args:
        itens: Lista de itens com campo 'tipo'

    Returns:
        Dicionário com contagem de arquivos e pastas
    """
    return {
        "arquivos": sum(1 for item in itens if item.get("tipo") == "arquivo"),
        "pastas": sum(1 for item in itens if item.get("tipo") == "pasta"),
        "total": len(itens),
    }


def filtrar_arquivos_por_extensao(
    itens: list[dict[str, Any]], extensao: str
) -> list[dict[str, Any]]:
    """
    Filtra arquivos por extensão em uma lista de itens.

    Args:
        itens: Lista de itens
        extensao: Extensão para filtrar (ex: '.pdf', '.txt')

    Returns:
        Lista filtrada de arquivos com a extensão
    """
    extensao = extensao.lower() if extensao.startswith(".") else f".{extensao.lower()}"

    return [
        item
        for item in itens
        if item.get("tipo") == "arquivo" and item.get("extensao", "").lower() == extensao
    ]


def resumir_conteudo_pasta(itens: list[dict[str, Any]], limite: int = 10) -> dict[str, Any]:
    """
    Cria um resumo do conteúdo de uma pasta.

    Args:
        itens: Lista de itens da pasta
        limite: Número máximo de itens no resumo

    Returns:
        Dicionário com resumo da pasta
    """
    contagem = contar_itens_por_tipo(itens)

    return {
        "quantidade_itens": contagem["total"],
        "quantidade_arquivos": contagem["arquivos"],
        "quantidade_pastas": contagem["pastas"],
        "primeiros_itens": itens[:limite],
        "ha_mais_itens": len(itens) > limite,
    }


def info_formatada_pasta(
    nome: str,
    quantidade_itens: int,
    tamanho_total: int,
    itens: list[dict[str, Any]] | None = None,
    inclui_subpastas: bool = False,
    permissoes: str = "755",
) -> dict[str, Any]:
    """
    Retorna informações formatadas de uma pasta.

    Args:
        nome: Nome da pasta
        quantidade_itens: Quantidade de itens
        tamanho_total: Tamanho total em bytes
        itens: Lista de itens (opcional)
        inclui_subpastas: Se inclui subpastas recursivamente
        permissoes: Permissões da pasta

    Returns:
        Dicionário com informações formatadas
    """
    info = {
        "nome": nome,
        "quantidade_itens": quantidade_itens,
        "tamanho_formatado": formatar_tamanho(tamanho_total),
        "tamanho_bytes": tamanho_total,
        "inclui_subpastas": inclui_subpastas,
        "permissoes": permissoes,
    }

    if itens is not None:
        info["conteudo_resumido"] = itens[:10]
        info["ha_mais_itens"] = len(itens) > 10
        info["quantidade_arquivos"] = sum(1 for i in itens if i.get("tipo") == "arquivo")
        info["quantidade_pastas"] = sum(1 for i in itens if i.get("tipo") == "pasta")

    return info
