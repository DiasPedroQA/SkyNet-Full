# pylint: disable=E0401
# pyright: reportCallIssue=false
# type: ignore[call-arg]

"""Modelo especializado para arquivos do sistema"""

from pathlib import Path

from pydantic import Field, field_validator
from services.formatadores import (
    eh_executavel,
    eh_imagem,
    eh_pdf,
    eh_texto,
    formatar_tamanho,
    identificar_tipo,
    obter_extensao,
)

from .comum_base import CaminhoBase


class ArquivoInfo(CaminhoBase):
    """
    Classe especializada para arquivos.
    Herda de CaminhoBase e usa os formatadores do módulo services.
    """

    # ========================================================================
    # ATRIBUTOS ESPECÍFICOS
    # ========================================================================
    tipo: str = Field("arquivo", description="Tipo do item (sempre 'arquivo')")
    linhas: int | None = Field(None, description="Número de linhas (para arquivos de texto)")

    # ========================================================================
    # VALIDADORES
    # ========================================================================
    @field_validator("caminho")
    @classmethod
    def validar_arquivo(cls, caminho_valor: str) -> str:
        """
        Valida se o caminho existe e é um arquivo.
        """
        caminho_validado = super().validar_caminho(caminho_valor)

        if not Path(caminho_validado).is_file():
            raise ValueError(f"O caminho '{caminho_valor}' não é um arquivo")

        return caminho_validado

    # ========================================================================
    # PROPRIEDADES COMPUTADAS (delegando para formatadores)
    # ========================================================================

    @property
    def extensao(self) -> str:
        """Retorna a extensão do arquivo."""
        return self.extensao or obter_extensao(self.caminho)

    @property
    def nome_sem_extensao(self) -> str:
        """Retorna o nome do arquivo sem a extensão."""
        if self.nome and self.extensao:
            return self.nome[: -len(self.extensao)]
        return self.nome or ""

    @property
    def tamanho_formatado_arquivo(self) -> str:
        """Retorna o tamanho formatado."""
        return formatar_tamanho(self.tamanho_bytes or 0)

    @property
    def tipo_identificado_arquivo(self) -> str:
        """Retorna o tipo identificado."""
        return identificar_tipo(self.caminho)

    # ========================================================================
    # MÉTODOS DE VERIFICAÇÃO (delegados)
    # ========================================================================

    def eh_pdf(self) -> bool:
        """Verifica se é um arquivo PDF."""
        return eh_pdf(self.extensao)

    def eh_imagem(self) -> bool:
        """Verifica se é uma imagem."""
        return eh_imagem(self.extensao)

    def eh_texto(self) -> bool:
        """Verifica se é um arquivo de texto."""
        return eh_texto(self.extensao)

    def eh_executavel(self) -> bool:
        """Verifica se o arquivo é executável."""
        return eh_executavel(self.extensao, self.permissoes or "")

    # ========================================================================
    # MÉTODOS DE ACESSO A DADOS (apenas passagem)
    # ========================================================================

    def obter_tamanho(self) -> int:
        """Retorna o tamanho do arquivo em bytes."""
        return self.tamanho_bytes or 0

    def obter_extensao(self) -> str:
        """Retorna a extensão do arquivo."""
        return self.extensao

    def obter_dono(self) -> str | None:
        """Retorna o dono do arquivo."""
        return self.dono

    # ========================================================================
    # MÉTODOS DE AÇÃO
    # ========================================================================

    def recarregar_arquivo(self) -> None:
        """Recarrega as propriedades do arquivo."""
        self.recarregar()

    # ========================================================================
    # MÉTODOS DE FORMATAÇÃO
    # ========================================================================

    def info_completa(self) -> dict[str, object]:
        """
        Retorna informações completas do arquivo.
        Combina dados da classe com informações formatadas.
        """
        info_base = self.info_detalhada.copy()
        info_formatada = self.info_formatada

        info_arquivo = {
            **info_base,
            **info_formatada,
            "linhas": self.linhas,
            "mime_type": self.mime_type,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
            "data_modificacao": self.data_modificacao.isoformat() if self.data_modificacao else None,
        }

        return {k: v for k, v in info_arquivo.items() if v is not None}

    # ========================================================================
    # REPRESENTAÇÕES
    # ========================================================================

    def __str__(self) -> str:
        """Representação em string amigável."""
        return f"📄 {self.nome} ({self.tamanho_formatado_arquivo}) - {self.tipo_identificado_arquivo}"

    def __repr__(self) -> str:
        """Representação para debug."""
        return f"ArquivoInfo(caminho='{self.caminho}', existe={self.existe})"
