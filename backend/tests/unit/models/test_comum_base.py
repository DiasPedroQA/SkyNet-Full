# pylint: disable=redefined-outer-name, line-too-long

"""Testes para o modelo base do sistema de arquivos."""

import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Generator, Optional, Set, Type, Union, get_args, get_origin, get_type_hints

import pytest

from app.infrastructure.models.comum_base import CaminhoBase

# ============================================================================
# FUNÇÕES GENÉRICAS DE VALIDAÇÃO DE CLASSES (REUTILIZÁVEIS)
# ============================================================================


def assert_class_has_attributes(cls: Type, atributos_esperados: Set[str]) -> None:
    """
    Verifica se a classe possui todos os atributos esperados.

    Args:
        cls: Classe a ser validada
        atributos_esperados: Conjunto de nomes de atributos obrigatórios
    """
    anotacoes = getattr(cls, "__annotations__", {})
    atributos_reais = set(anotacoes.keys())

    faltantes = atributos_esperados - atributos_reais
    assert not faltantes, f"Atributos faltando na classe {cls.__name__}: {faltantes}"


def assert_class_attributes_types(
    cls: Type, tipos_esperados: dict[str, str | int | bool | list | datetime | None]
) -> None:
    """
    Verifica se a classe possui os atributos com os tipos corretos.

    Args:
        cls: Classe a ser validada
        tipos_esperados: Dicionário com {nome_atributo: tipo_esperado}
    """
    # Usa get_type_hints para resolver tipos como Union, etc.
    dicas_tipo = get_type_hints(cls)

    # Verifica atributos faltantes
    atributos_esperados = set(tipos_esperados.keys())
    atributos_reais = set(dicas_tipo.keys())
    faltantes = atributos_esperados - atributos_reais

    if faltantes:
        existentes = {attr for attr in faltantes if hasattr(cls, attr)}
        if existentes:
            faltantes = faltantes - existentes

        if faltantes:
            raise AssertionError(f"Atributos faltando na classe {cls.__name__}: {faltantes}")

    # Verifica tipos
    tipos_incorretos = {}
    for attr, tipo_esperado in tipos_esperados.items():
        if attr in dicas_tipo:
            tipo_real = dicas_tipo[attr]
            if tipo_real != tipo_esperado:
                tipos_incorretos[attr] = (tipo_real, tipo_esperado)

    assert not tipos_incorretos, (
        f"Tipos incorretos na classe {cls.__name__}: "
        f"{ {attr: f'recebido {real}, esperado {esp}' for attr, (real, esp) in tipos_incorretos.items()} }"
    )


def assert_instance_attributes_types(
    instancia: Any, tipos_esperados: dict[str, str | int | bool | list | datetime | None]
) -> None:
    """
    Verifica se a instância possui os atributos com valores do tipo correto.

    Args:
        instancia: Instância a ser validada
        tipos_esperados: Dicionário com {nome_atributo: tipo_esperado}
    """
    for attr, tipo_esperado in tipos_esperados.items():
        assert hasattr(instancia, attr), f"Atributo '{attr}' não existe na instância"
        valor = getattr(instancia, attr)

        if valor is not None and get_origin(tipo_esperado) is Union:
            tipos_permitidos = get_args(tipo_esperado)
            assert isinstance(valor, tipos_permitidos), (
                f"Atributo '{attr}': esperado {tipos_permitidos}, "
                f"recebido {type(valor).__name__ if valor is not None else 'None'}"
            )


# ============================================================================
# FUNÇÕES AUXILIARES DE VALIDAÇÃO (REUTILIZÁVEIS)
# ============================================================================


def validar_propriedades_arquivo(modelo: CaminhoBase, nome_esperado: str, tamanho_minimo: int = 0) -> None:
    """Valida propriedades básicas de um arquivo."""
    assert modelo.nome == nome_esperado
    assert modelo.tipo == "arquivo"
    assert isinstance(modelo.tamanho_bytes, int)
    assert modelo.tamanho_bytes >= tamanho_minimo
    assert modelo.existe is True


def validar_propriedades_pasta(modelo: CaminhoBase, nome_esperado: str) -> None:
    """Valida propriedades básicas de uma pasta."""
    assert modelo.nome == nome_esperado
    assert modelo.tipo == "pasta"
    assert modelo.existe is True
    assert modelo.extensao in (None, "")


def validar_datas(modelo: CaminhoBase) -> None:
    """Valida se as datas estão presentes e são do tipo correto."""
    assert modelo.data_modificacao is not None
    assert modelo.data_criacao is not None
    assert modelo.data_acesso is not None
    assert isinstance(modelo.data_modificacao, datetime)
    assert isinstance(modelo.data_criacao, datetime)
    assert isinstance(modelo.data_acesso, datetime)


def validar_estatisticas_completas(modelo: CaminhoBase) -> None:
    """Valida todas as estatísticas do sistema de arquivos."""
    assert modelo.permissoes is not None
    assert len(modelo.permissoes) == 3  # formato octal
    assert modelo.dono is not None
    assert modelo.mime_type is not None


def validar_caminho_resolvido(modelo: CaminhoBase, caminho_original: Path) -> None:
    """Valida se o caminho foi resolvido corretamente."""
    assert Path(str(modelo.caminho)) == caminho_original.resolve()


def validar_modelo_inexistente(modelo: CaminhoBase, nome_esperado: str) -> None:
    """Valida propriedades de um modelo com caminho inexistente."""
    assert Path(str(modelo.caminho)).name == nome_esperado
    assert modelo.nome is None
    assert modelo.tamanho_bytes == 0
    assert modelo.data_modificacao is None
    assert modelo.data_criacao is None
    assert modelo.data_acesso is None
    assert modelo.existe is False


def validar_modelo_com_erro_permissao(modelo: CaminhoBase) -> None:
    """Valida propriedades de um modelo com erro de permissão."""
    assert modelo.tamanho_bytes == 0
    assert modelo.data_criacao is None
    assert modelo.data_modificacao is None
    assert modelo.data_acesso is None
    assert modelo.permissoes is None
    assert modelo.dono is None
    assert modelo.existe is True


# ============================================================================
# FIXTURES COMPARTILHADAS
# ============================================================================


@pytest.fixture
def arquivo_temporario() -> Generator[Path, None, None]:
    """Fixture que cria um arquivo temporário único."""
    with tempfile.NamedTemporaryFile(delete=False) as arquivo_temp:
        arquivo_temp.write(b"conteudo de teste")
        arquivo_temp.flush()
        caminho_arquivo = Path(arquivo_temp.name)
        yield caminho_arquivo
    os.unlink(caminho_arquivo)


@pytest.fixture
def diretorio_temporario() -> Generator[Path, None, None]:
    """Fixture que cria um diretório temporário."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def arquivo_e_pasta_teste(diretorio_temporario: Path) -> tuple[Path, Path]:
    """Fixture que cria um arquivo e uma pasta para testes."""
    arquivo = diretorio_temporario / "documento.txt"
    arquivo.write_text("conteúdo de teste")

    pasta = diretorio_temporario / "subpasta"
    pasta.mkdir()

    return arquivo, pasta


# ============================================================================
# TESTES DA ESTRUTURA DA CLASSE (VALIDAM A CLASSE EM SI)
# ============================================================================


class TestEstruturaCaminhoBase:
    """Testes para validar a estrutura da classe CaminhoBase."""

    def test_classe_possui_todos_atributos_obrigatorios(self) -> None:
        """Verifica se a classe CaminhoBase possui todos os atributos necessários."""
        atributos_esperados = {
            "caminho",
            "nome",
            "tipo",
            "existe",
            "tamanho_bytes",
            "data_criacao",
            "data_modificacao",
            "data_acesso",
            "oculto",
            "permissoes",
            "dono",
            "pai",
            "extensao",
            "mime_type",
            "linhas",
            "itens",
            "quantidade_itens",
            "tamanho_total",
        }
        assert_class_has_attributes(CaminhoBase, atributos_esperados)

    def test_classe_possui_tipos_corretos(self) -> None:
        """Verifica se os tipos dos atributos estão corretos."""

        # CORREÇÃO: dict[str, type] em vez de dict[str, tipos]
        tipos_esperados: dict = {
            "caminho": str,
            "nome": Optional[str],
            "tipo": Optional[str],
            "existe": bool,
            "tamanho_bytes": Optional[int],
            "data_criacao": Optional[datetime],
            "data_modificacao": Optional[datetime],
            "data_acesso": Optional[datetime],
            "oculto": Optional[bool],
            "permissoes": Optional[str],
            "dono": Optional[str],
            "pai": Optional[str],
            "extensao": Optional[str],
            "mime_type": Optional[str],
            "linhas": Optional[int],
            "itens": list,
            "quantidade_itens": Optional[int],
            "tamanho_total": Optional[int],
        }
        assert_class_attributes_types(CaminhoBase, tipos_esperados)

    def test_propriedades_adicionais_arquivo(self, diretorio_temporario: Path) -> None:
        """Testa se permissoes, dono e mime_type são carregados."""
        arquivo = diretorio_temporario / "teste.txt"
        arquivo.write_text("conteudo")

        modelo = CaminhoBase(caminho=arquivo)
        validar_estatisticas_completas(modelo)

        # CORREÇÃO: Verificação antes de usar startswith
        assert modelo.mime_type is not None
        assert modelo.mime_type.startswith("text/")

    # Testes para casos especiais e integração
    def test_info_detalhada_chaves_obrigatorias(self, diretorio_temporario: Path) -> None:
        """info_detalhada deve conter todas as chaves esperadas."""
        arquivo = diretorio_temporario / "informacoes.txt"
        arquivo.write_text("dados")

        modelo = CaminhoBase(caminho=arquivo)
        chaves = {"caminho", "nome", "tipo", "existe", "tamanho_bytes", "extensao", "pai", "itens"}
        assert chaves.issubset(set(modelo.info_detalhada.keys()))


# ============================================================================
# TESTES BÁSICOS (INDEPENDENTES DE TIPO)
# ============================================================================


class TestCaminhoBaseBasico:
    """Testes básicos da classe CaminhoBase."""

    def test_criar_modelo_com_caminho_inexistente(self) -> None:
        """Deve criar modelo com valores default quando caminho não existe."""
        caminho_inexistente = Path("/caminho/invalido/arquivo.txt")
        modelo = CaminhoBase(caminho=caminho_inexistente)
        validar_modelo_inexistente(modelo, "arquivo.txt")

    def test_obter_caminho_pai(self, arquivo_temporario: Path) -> None:
        """Deve retornar o diretório pai do caminho atual."""
        modelo = CaminhoBase(caminho=arquivo_temporario)
        assert modelo.pai is not None
        assert Path(modelo.pai) == arquivo_temporario.parent

    def test_detectar_arquivo_oculto(self, diretorio_temporario: Path) -> None:
        """Deve identificar corretamente arquivos ocultos."""
        # Arquivo normal
        arquivo_normal = diretorio_temporario / "visivel.txt"
        arquivo_normal.touch()
        assert CaminhoBase(caminho=arquivo_normal).oculto is False

        # Arquivo oculto
        arquivo_oculto = diretorio_temporario / ".config"
        arquivo_oculto.touch()
        assert CaminhoBase(caminho=arquivo_oculto).oculto is True

    def test_validar_caminho_com_entradas_variadas(self) -> None:
        """Testa o validador de caminho com diferentes entradas."""
        with pytest.raises(ValueError):
            CaminhoBase(caminho="")

        with pytest.raises(ValueError):
            CaminhoBase(caminho=None)

        caminho_path = Path("/home/teste")
        modelo = CaminhoBase(caminho=caminho_path)
        assert modelo.caminho == str(caminho_path.expanduser().resolve(strict=False))


# ============================================================================
# TESTES ESPECÍFICOS PARA ARQUIVOS
# ============================================================================


class TestCaminhoBaseArquivo:
    """Testes específicos para funcionalidades de arquivo."""

    def test_criar_modelo_com_arquivo_valido(self, arquivo_temporario: Path) -> None:
        """Deve criar modelo corretamente quando o caminho existe."""
        modelo = CaminhoBase(caminho=arquivo_temporario)

        validar_caminho_resolvido(modelo, arquivo_temporario)
        validar_propriedades_arquivo(modelo, arquivo_temporario.name)
        validar_datas(modelo)
        validar_estatisticas_completas(modelo)

    def test_contar_linhas_em_arquivo_texto(self, diretorio_temporario: Path) -> None:
        """Testa a contagem de linhas para arquivos de texto."""
        arquivo = diretorio_temporario / "multilinhas.txt"
        conteudo = "primeira linha\nsegunda linha\nterceira linha\n"
        arquivo.write_text(conteudo, encoding="utf-8")

        modelo = CaminhoBase(caminho=arquivo)
        assert modelo.linhas == conteudo.count("\n")
        assert modelo.info_completa() == modelo.info_detalhada

    def test_carregar_arquivo_nao_texto(self, diretorio_temporario: Path) -> None:
        """Testa carregamento de arquivo binário."""
        arquivo = diretorio_temporario / "dados.bin"
        arquivo.write_bytes(b"\x00\x01\x02\x03")

        modelo = CaminhoBase(caminho=arquivo)
        assert modelo.linhas is None
        assert modelo.mime_type is not None

    def test_propriedades_adicionais_arquivo(self, diretorio_temporario: Path) -> None:
        """Testa se permissoes, dono e mime_type são carregados."""
        arquivo = diretorio_temporario / "teste.txt"
        arquivo.write_text("conteudo")

        modelo = CaminhoBase(caminho=arquivo)
        validar_estatisticas_completas(modelo)
        if isinstance(modelo.mime_type, str):
            assert modelo.mime_type.startswith("text/")


# ============================================================================
# TESTES ESPECÍFICOS PARA PASTAS
# ============================================================================


class TestCaminhoBasePasta:
    """Testes específicos para funcionalidades de pasta."""

    def test_criar_modelo_com_pasta_valida(self, diretorio_temporario: Path) -> None:
        """Deve criar modelo corretamente para uma pasta."""
        pasta = diretorio_temporario / "minha_pasta"
        pasta.mkdir()

        modelo = CaminhoBase(caminho=pasta)
        validar_propriedades_pasta(modelo, "minha_pasta")
        validar_datas(modelo)

    def test_quantidade_itens_em_pasta(self, diretorio_temporario: Path) -> None:
        """Testa se quantidade_itens conta corretamente."""
        pasta = diretorio_temporario / "minha_pasta"
        pasta.mkdir()

        for i in range(3):
            (pasta / f"arquivo{i}.txt").write_text("teste")

        modelo = CaminhoBase(caminho=pasta)
        assert modelo.quantidade_itens == 3
        assert len(modelo.itens) == 3

    def test_tamanho_total_soma_arquivos_na_pasta(self, diretorio_temporario: Path) -> None:
        """tamanho_total deve somar bytes de todos arquivos na pasta."""
        diretorio = diretorio_temporario / "pasta_com_arquivos"
        diretorio.mkdir()

        (diretorio / "pequeno.bin").write_bytes(b"abc")  # 3 bytes
        (diretorio / "medio.bin").write_bytes(b"12345")  # 5 bytes

        modelo = CaminhoBase(caminho=diretorio)
        assert modelo.tamanho_total == 8
        assert modelo.tamanho_bytes == 8

    def test_propriedade_is_pasta(self, diretorio_temporario: Path) -> None:
        """Verifica se a propriedade is_pasta funciona corretamente."""
        diretorio = diretorio_temporario / "minha_pasta"
        diretorio.mkdir()
        arquivo = diretorio_temporario / "meu_arquivo.txt"
        arquivo.write_text("x")

        assert CaminhoBase(caminho=diretorio).is_pasta is True
        assert CaminhoBase(caminho=arquivo).is_pasta is False
