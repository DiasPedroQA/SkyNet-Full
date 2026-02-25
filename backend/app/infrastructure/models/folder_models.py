# pylint: disable=too-many-instance-attributes, wrong-import-order, import-error, line-too-long
# pyright: reportCallIssue=false

"""Modelo especializado para pastas/diretórios do sistema"""

import contextlib
from pathlib import Path

from pydantic import Field, field_validator
from services.formatadores import (
    contar_itens_por_tipo,
    filtrar_arquivos_por_extensao,
    formatar_tamanho,
    resumir_conteudo_pasta,
)

from .comum_base import CaminhoBase
from .file_models import ArquivoInfo


class PastaInfo(CaminhoBase):
    """
    Classe especializada para pastas/diretórios.
    Herda de CaminhoBase e usa os formatadores do módulo services.
    """

    # ========================================================================
    # ATRIBUTOS ESPECÍFICOS
    # ========================================================================
    tipo: str = Field("pasta", description="Tipo do item (sempre 'pasta')")
    incluir_subpastas: bool = Field(False, description="Se deve incluir recursivamente o conteúdo das subpastas")
    objetos_itens: list[Union[ArquivoInfo, "PastaInfo"]] = Field(
        default_factory=list, description="Lista de objetos dos itens da pasta"
    )
    permissoes: str = Field("755", description="Permissões da pasta em formato octal")

    def __init__(self, **data):
        """Inicializa PastaInfo - apenas 'caminho' é realmente necessário."""
        super().__init__(**data)
        if self.existe and self.is_pasta:
            self._carregar_conteudo_pasta()

    # ========================================================================
    # VALIDADORES
    # ========================================================================
    @field_validator("caminho")
    @classmethod
    def validar_pasta(cls, caminho_valor: str) -> str:
        """Valida se o caminho existe e é uma pasta."""
        caminho_validado = super().validar_caminho(caminho_valor)

        if not Path(caminho_validado).is_dir():
            raise ValueError(f"O caminho '{caminho_valor}' não é uma pasta")

        return caminho_validado

    # ========================================================================
    # PROPRIEDADES COMPUTADAS
    # ========================================================================

    @property
    def info_resumida_pasta(self) -> dict[str, object]:
        """Versão resumida específica para pastas."""
        info = self.info_resumida.copy()

        # Usa função do formatadores para contar itens
        contagem = contar_itens_por_tipo(self.itens)

        info.update({
            "quantidade_arquivos": contagem["arquivos"],
            "quantidade_pastas": contagem["pastas"],
            "tamanho_formatado": self.tamanho_formatado,
            "inclui_subpastas": self.incluir_subpastas,
        })
        return info

    @property
    def conteudo_simples(self) -> list[dict[str, object]]:
        """Lista o conteúdo de forma simplificada."""
        if not self.is_pasta:
            return []

        def extrair_dados_seguro(item: dict[str, object]) -> dict[str, object]:
            """Extrai dados do item com conversão de tipos segura."""
            return {
                "nome": str(item.get("nome", "")),
                "tipo": str(item.get("tipo", "")),
                "oculto": bool(item.get("oculto", False)),
                "tamanho": item.get("tamanho") if isinstance(item.get("tamanho"), (int, type(None))) else None,
                "tamanho_formatado": str(item.get("tamanho_formatado"))
                if item.get("tamanho_formatado") is not None
                else None,
                "extensao": str(item.get("extensao")) if item.get("extensao") is not None else None,
                "modificado": str(item.get("modificado")) if item.get("modificado") is not None else None,
            }

        return [extrair_dados_seguro(item) for item in self.itens]

    # ========================================================================
    # MÉTODOS DE CARREGAMENTO
    # ========================================================================

    def _carregar_conteudo_pasta(self) -> None:
        """Carrega o conteúdo da pasta usando os dados já disponíveis."""
        if not self._path_obj:
            return

        self.objetos_itens = []

        for item_info in self.itens:
            nome_item = item_info.get("nome", "")
            if not nome_item or not isinstance(nome_item, str):
                continue

            caminho_completo = self._path_obj / nome_item

            try:
                if item_info.get("tipo") == "arquivo":
                    item_obj = ArquivoInfo(caminho=str(caminho_completo))
                elif item_info.get("tipo") == "pasta":
                    item_obj = PastaInfo(caminho=str(caminho_completo))
                else:
                    continue

                self.objetos_itens.append(item_obj)

            except (ValueError, OSError):
                continue

    # ========================================================================
    # MÉTODOS DE LISTAGEM E CONTAGEM
    # ========================================================================

    def listar_conteudo(self, apenas_nomes: bool = False) -> list[str]:
        """Lista o conteúdo da pasta."""
        if not self._path_obj:
            return []

        if self.incluir_subpastas:
            if apenas_nomes:
                return [p.name for p in self._path_obj.rglob("*")]
            return [str(p.relative_to(self.caminho)) for p in self._path_obj.rglob("*")]
        else:
            if apenas_nomes:
                return [p.name for p in self._path_obj.iterdir()]
            return [p.name for p in self._path_obj.iterdir()]

    def contar_arquivos(self) -> int:
        """Conta o número de arquivos na pasta."""
        if self.objetos_itens:
            return sum(1 for obj in self.objetos_itens if isinstance(obj, ArquivoInfo))

        # Usa a função do formatadores
        contagem = contar_itens_por_tipo(self.itens)
        return contagem["arquivos"]

    def contar_pastas(self) -> int:
        """Conta o número de subpastas."""
        if self.objetos_itens:
            return sum(1 for obj in self.objetos_itens if isinstance(obj, PastaInfo))

        # Usa a função do formatadores
        contagem = contar_itens_por_tipo(self.itens)
        return contagem["pastas"]

    def calcular_tamanho_total(self) -> int:
        """Calcula o tamanho total de todos os arquivos na pasta."""
        if self.tamanho_total is not None:
            return self.tamanho_total

        total = 0
        if self._path_obj:
            for arquivo in self._path_obj.rglob("*"):
                if arquivo.is_file():
                    with contextlib.suppress(OSError, PermissionError):
                        total += arquivo.stat().st_size

        self.tamanho_total = total
        return total

    # ========================================================================
    # MÉTODOS DE BUSCA E FILTRO
    # ========================================================================

    def encontrar_por_nome(self, nome_busca: str) -> dict[str, object] | None:
        """Encontra um item na pasta pelo nome."""
        for item in self.itens:
            if item.get("nome") == nome_busca:
                return item
        return None

    def encontrar_objeto_por_nome(self, nome_busca: str) -> Union[ArquivoInfo, "PastaInfo", None]:
        """Encontra um objeto na pasta pelo nome."""
        for obj in self.objetos_itens:
            if obj.nome == nome_busca:
                return obj
        return None

    def listar_arquivos_por_extensao(self, extensao: str) -> list[dict[str, object]]:
        """Lista todos os arquivos com determinada extensão."""
        return filtrar_arquivos_por_extensao(self.itens, extensao)

    # ========================================================================
    # MÉTODOS DE MANIPULAÇÃO
    # ========================================================================

    def adicionar_item(self, novo_item: Union[ArquivoInfo, "PastaInfo", dict[str, object]]) -> None:
        """Adiciona um item à pasta (em memória)."""
        if isinstance(novo_item, (PastaInfo, ArquivoInfo)):
            self.objetos_itens.append(novo_item)

            # Usa formatador para criar o dicionário do item com tipos seguros
            item_dict = formatar_info_item_pasta(
                nome=str(novo_item.nome or ""),
                tipo=str(novo_item.tipo),
                oculto=bool(novo_item.oculto or False),
                tamanho=novo_item.tamanho_bytes if isinstance(novo_item.tamanho_bytes, (int, type(None))) else None,
                tamanho_formatado=str(novo_item.tamanho_formatado) if novo_item.tamanho_formatado is not None else None,
                extensao=str(getattr(novo_item, "extensao", None))
                if getattr(novo_item, "extensao", None) is not None
                else None,
                modificado=novo_item.data_modificacao.isoformat() if novo_item.data_modificacao else None,
            )
            self.itens.append(item_dict)

        elif isinstance(novo_item, dict):
            # Converte tipos do dicionário para serem seguros
            item_seguro = {
                "nome": str(novo_item.get("nome", "")),
                "tipo": str(novo_item.get("tipo", "")),
                "oculto": bool(novo_item.get("oculto", False)),
                "tamanho": novo_item.get("tamanho")
                if isinstance(novo_item.get("tamanho"), (int, type(None)))
                else None,
                "tamanho_formatado": str(novo_item.get("tamanho_formatado"))
                if novo_item.get("tamanho_formatado") is not None
                else None,
                "extensao": str(novo_item.get("extensao")) if novo_item.get("extensao") is not None else None,
                "modificado": str(novo_item.get("modificado")) if novo_item.get("modificado") is not None else None,
            }
            self.itens.append(item_seguro)

        self.quantidade_itens = len(self.itens)
        self._atualizar_tamanho_total()

    def remover_item(self, nome_item: str) -> bool:
        """Remove um item da pasta pelo nome."""
        tamanho_inicial = len(self.itens)

        self.itens = [item for item in self.itens if item.get("nome") != nome_item]
        self.objetos_itens = [obj for obj in self.objetos_itens if obj.nome != nome_item]

        removido = len(self.itens) < tamanho_inicial
        if removido:
            self.quantidade_itens = len(self.itens)
            self._atualizar_tamanho_total()

        return removido

    def _atualizar_tamanho_total(self):
        """Atualiza o tamanho total baseado nos itens."""
        self.tamanho_total = sum(
            obj.tamanho_bytes or 0
            for obj in self.objetos_itens
            if isinstance(obj, ArquivoInfo) and isinstance(obj.tamanho_bytes, (int, type(None)))
        )
        self.tamanho_bytes = self.tamanho_total

    # ========================================================================
    # MÉTODOS DE INFORMAÇÃO
    # ========================================================================

    def info_completa(self) -> dict[str, object]:
        """Retorna informações completas da pasta."""
        info_base = self.info_detalhada.copy()

        # Usa a função de resumo do formatadores
        resumo = resumir_conteudo_pasta(self.itens, limite=10)

        info_pasta = {
            **info_base,
            **resumo,
            "tamanho_total_bytes": self.calcular_tamanho_total(),
            "tamanho_formatado": formatar_tamanho(self.tamanho_total or 0),
            "inclui_subpastas": self.incluir_subpastas,
            "permissoes": self.permissoes,
        }

        return {k: v for k, v in info_pasta.items() if v is not None}

    # ========================================================================
    # REPRESENTAÇÕES
    # ========================================================================

    def __str__(self) -> str:
        """Representação em string amigável."""
        return f"📁 {self.nome} ({self.quantidade_itens} itens, {self.tamanho_formatado})"

    def __repr__(self) -> str:
        """Representação para debug."""
        return f"PastaInfo(caminho='{self.caminho}', existe={self.existe})"
