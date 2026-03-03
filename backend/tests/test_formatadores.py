# pylint: disable=line-too-long

"""Módulo de teste unitário para os formatadores do sistema de arquivos"""

from pathlib import Path
from typing import Literal

import pytest

from app.infrastructure.services.formatadores import formatar_tamanho_arquivo, is_oculto, obter_extensao


class TestFuncoesAuxiliares:
    """Testes para as funções auxiliares de sistema de arquivos."""

    @pytest.mark.parametrize(
        "nome,esperado",
        [
            (".gitignore", True),
            (".env", True),
            ("arquivo.txt", False),
            ("pasta/", False),
            (".", True),
            ("..", True),
            (__file__, False),
        ],
    )
    def test_is_oculto(self, nome: str, esperado: bool) -> None:
        """Testa a função is_oculto."""
        assert is_oculto(nome) == esperado

    @pytest.mark.parametrize(
        "caminho,esperado",
        [
            ("arquivo.txt", ".txt"),
            ("imagem.JPG", ".jpg"),
            ("sem_extensao", ""),
            ("pasta/", ""),
            (Path("documento.pdf"), ".pdf"),
            (Path("script.PY"), ".py"),
            (Path("README"), ""),
            (__file__, ".py"),
        ],
    )
    def test_obter_extensao(
        self,
        caminho: Path | str,
        esperado: str | Literal[""],
    ) -> None:
        """Testa a função obter_extensao."""
        assert obter_extensao(caminho) == esperado

    @pytest.mark.parametrize(
        "tamanho,esperado",
        [
            (0.5, "0 B"),
            (500.5, "500 B"),
            (1023.5, "1023 B"),
            (1024.5, "1.0 KB"),
            (2048.5, "2.0 KB"),
            (1500.5, "1.5 KB"),
            (1024 * 1024, "1.0 MB"),
            (3 * 1024 * 1024, "3.0 MB"),
            (1_500_000.5, "1.4 MB"),
            (1024 * 1024 * 1024, "1.0 GB"),
            (2_500_000_000.5, "2.3 GB"),
        ],
    )
    def test_formatar_tamanho_arquivo(self, tamanho: float, esperado: str) -> None:
        """Testa a função formatar_tamanho_arquivo."""
        assert formatar_tamanho_arquivo(tamanho) == esperado
