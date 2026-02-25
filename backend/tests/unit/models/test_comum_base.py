"""Testes para o modelo base comum."""

import os
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from app.infrastructure.models.comum_base import CaminhoBase


class TestCaminhoBase:
    """Testes para a classe CaminhoBase."""

    def test_caminho_base_criacao_com_path_valido(self) -> None:
        """Testa criação com path válido."""
        with tempfile.NamedTemporaryFile() as tmp:
            path = Path(tmp.name)
            modelo = CaminhoBase(caminho=path)

            assert Path(str(modelo.caminho)) == path.resolve()
            assert modelo.nome == path.name
            assert isinstance(modelo.tamanho_bytes, int)
            assert modelo.tamanho_bytes >= 0
            assert modelo.data_modificacao is not None
            assert modelo.data_criacao is not None
            assert isinstance(modelo.data_modificacao, datetime)
            assert isinstance(modelo.data_criacao, datetime)

    def test_caminho_base_criacao_com_path_inexistente(self) -> None:
        """Testa criação com path inexistente."""
        path = Path("/caminho/inexistente/arquivo.txt")
        modelo = CaminhoBase(caminho=path)

        # Caminho pode ser normalizado para string; verificar nome e comportamento quando não existe
        assert Path(str(modelo.caminho)).name == "arquivo.txt"
        assert modelo.nome is None  # O nome é None quando o caminho não existe
        assert modelo.tamanho_bytes == 0
        assert modelo.data_modificacao is None
        assert modelo.data_criacao is None

    def test_caminho_base_todos_atributos(self) -> None:
        """Testa se todos os atributos esperados estão presentes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Criar arquivo real para teste
            arquivo_real = Path(tmpdir) / "teste.txt"
            arquivo_real.write_text("conteúdo de teste")

            # Criar pasta real
            pasta_real = Path(tmpdir) / "pasta_teste"
            pasta_real.mkdir()

            # Dados para testar
            casos_teste = [arquivo_real, pasta_real]

            for path in casos_teste:
                modelo = CaminhoBase(caminho=path)
                esperado_attrs = [
                    "caminho",
                    "nome",
                    "tamanho_bytes",
                    "data_modificacao",
                    "data_criacao",
                    "oculto",
                    "extensao",
                    "pai",
                ]
                for attr in esperado_attrs:
                    assert hasattr(modelo, attr)

                if path.is_file():
                    assert modelo.tamanho_bytes is not None
                    assert modelo.tamanho_bytes > 0
                    assert modelo.extensao == ".txt"
                else:
                    # para pastas a extensão normalmente é None ou vazia
                    assert modelo.extensao in (None, "")

    def test_is_oculto(self) -> None:
        """Testa detecção de arquivos ocultos."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Arquivo não oculto
            arquivo_normal = Path(tmpdir) / "normal.txt"
            arquivo_normal.touch()
            modelo_normal = CaminhoBase(caminho=arquivo_normal)
            assert modelo_normal.oculto is False

            # Arquivo oculto (começa com .)
            arquivo_oculto = Path(tmpdir) / ".oculto.txt"
            arquivo_oculto.touch()
            modelo_oculto = CaminhoBase(caminho=arquivo_oculto)
            assert modelo_oculto.oculto is True

    def test_caminho_pai(self) -> None:
        """Testa obtenção do caminho pai."""
        with tempfile.NamedTemporaryFile() as tmp:
            modelo = CaminhoBase(caminho=Path(tmp.name))
            assert modelo.pai is not None
            assert Path(modelo.pai) == Path(tmp.name).parent


@pytest.fixture
def arquivo_temporario_unico_fixture():
    """Fixture que fornece um arquivo temporário único (evita redefinições)."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"teste")
        tmp.flush()
        yield Path(tmp.name)
    os.unlink(tmp.name)


def test_caminho_base_com_fixture(arquivo_temporario_unico_fixture) -> None:
    """Teste usando fixture única."""
    modelo = CaminhoBase(caminho=arquivo_temporario_unico_fixture)
    assert modelo.tamanho_bytes is not None
    assert modelo.tamanho_bytes > 0
    assert modelo.nome == arquivo_temporario_unico_fixture.name


def test_listar_conteudo_simples_e_buscar_por_nome() -> None:
    """Testa listar_conteudo_simples e buscar_por_nome em pasta."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        f1 = d / "arquivoA.txt"
        f2 = d / "Outro.txt"
        sub = d / "subpasta"
        f1.write_text("linha1\nlinha2")
        f2.write_text("conteudo")
        sub.mkdir()

        modelo = CaminhoBase(caminho=d)
        simples = modelo.listar_conteudo_simples()
        nomes = {item["nome"] for item in simples}
        assert "arquivoA.txt" in nomes and "Outro.txt" in nomes and "subpasta" in nomes

        resultados = modelo.buscar_por_nome("arquivo")
        assert any(r["nome"] == "arquivoA.txt" for r in resultados)
        resultados_case = modelo.buscar_por_nome("OUTRO")
        assert any(r["nome"] == "Outro.txt" for r in resultados_case)
        # caminho_completo deve existir quando possível
        for r in resultados + resultados_case:
            assert str(Path(r["caminho_completo"]).parent) == str(d)


def test_mudar_caminho_e_recarregar(tmp_path) -> None:
    """Testa mudar_caminho e recarregar."""
    inexist = tmp_path / "nao_existe.txt"
    modelo = CaminhoBase(caminho=inexist)
    assert modelo.existe is False

    real = tmp_path / "real.txt"
    real.write_text("ok")
    ok = modelo.mudar_caminho(str(real))
    assert ok is True
    assert modelo.existe is True
    assert modelo.nome == real.name

    # voltar para inexistente
    ok2 = modelo.mudar_caminho(str(inexist))
    assert ok2 is False
    assert modelo.existe is False


def test_contar_linhas_e_linhas_valor(tmp_path) -> None:
    """Testa contagem de linhas para arquivos de texto."""
    f = tmp_path / "linhas.txt"
    content = "uma\nduas\ntrês\n"
    f.write_text(content, encoding="utf-8")
    modelo = CaminhoBase(caminho=f)
    assert modelo.linhas == content.count("\n")
    # garantir que info_completa delega para info_detalhada
    assert modelo.info_completa() == modelo.info_detalhada


def test_is_pasta_property(tmp_path) -> None:
    """Verifica is_pasta True para diretorio e False para arquivo."""
    d = tmp_path / "pasta"
    d.mkdir()
    f = tmp_path / "arquivo.txt"
    f.write_text("x")

    mod_d = CaminhoBase(caminho=d)
    mod_f = CaminhoBase(caminho=f)
    assert mod_d.is_pasta is True
    assert mod_f.is_pasta is False


def test_listar_conteudo_simples_em_arquivo(tmp_path) -> None:
    """Listar conteúdo simples em arquivo deve retornar lista vazia."""
    f = tmp_path / "arquivo.txt"
    f.write_text("x")
    modelo = CaminhoBase(caminho=f)
    assert modelo.listar_conteudo_simples() == []


def test_buscar_por_nome_em_arquivo_retorna_vazio(tmp_path) -> None:
    f = tmp_path / "arquivo.txt"
    f.write_text("conteudo")
    modelo = CaminhoBase(caminho=f)
    assert modelo.buscar_por_nome("arquivo") == []


def test_listar_conteudo_simples_tamanho_apenas_em_arquivos(tmp_path) -> None:
    d = tmp_path / "diretorio"
    d.mkdir()
    arq = d / "a.txt"
    arq.write_text("12345")
    sub = d / "subdir"
    sub.mkdir()

    modelo = CaminhoBase(caminho=d)
    simples = modelo.listar_conteudo_simples()
    by_name = {item["nome"]: item for item in simples}
    assert "a.txt" in by_name and "subdir" in by_name
    assert "tamanho" in by_name["a.txt"]
    assert "tamanho" not in by_name["subdir"]


def test_tamanho_total_soma_arquivos(tmp_path) -> None:
    d = tmp_path / "p"
    d.mkdir()
    f1 = d / "f1.bin"
    f2 = d / "f2.bin"
    f1.write_bytes(b"aaa")  # 3 bytes
    f2.write_bytes(b"bb")  # 2 bytes

    modelo = CaminhoBase(caminho=d)
    assert modelo.tamanho_total == 5
    assert modelo.tamanho_bytes == 5


def test_contar_linhas_latin1(tmp_path) -> None:
    f = tmp_path / "latin1.txt"
    content = "á\nb\n"
    f.write_text(content, encoding="latin-1")
    modelo = CaminhoBase(caminho=f)
    assert modelo.linhas == content.count("\n")


def test_info_detalhada_contem_chaves_esperadas(tmp_path) -> None:
    f = tmp_path / "x.txt"
    f.write_text("x")
    modelo = CaminhoBase(caminho=f)
    esperado = {"caminho", "nome", "tipo", "existe", "tamanho_bytes", "extensao", "pai", "itens"}
    assert esperado.issubset(set(modelo.info_detalhada.keys()))


def test_recarregar_atualiza_tamanho_bytes(tmp_path) -> None:
    f = tmp_path / "mod.txt"
    f.write_text("1")
    modelo = CaminhoBase(caminho=f)
    inicial = modelo.tamanho_bytes
    f.write_text("1" * 100)
    modelo.recarregar()
    assert modelo.tamanho_bytes is not None and modelo.tamanho_bytes > inicial
