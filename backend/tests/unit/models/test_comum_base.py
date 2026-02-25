# pylint: disable=redefined-outer-name

"""Testes para o modelo base do sistema de arquivos."""

import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Generator

import pytest

from app.infrastructure.models.comum_base import CaminhoBase


class TestCaminhoBase:
    """Suite de testes para a classe CaminhoBase (representação de arquivos/pastas)."""

    def test_criar_modelo_com_arquivo_valido(self) -> None:
        """Deve criar modelo corretamente quando o caminho existe."""
        with tempfile.NamedTemporaryFile() as arquivo_temporario:
            caminho_existente = Path(arquivo_temporario.name)
            modelo_arquivo = CaminhoBase(caminho=caminho_existente)

            # Verifica se o caminho é resolvido corretamente
            assert Path(str(modelo_arquivo.caminho)) == caminho_existente.resolve()

            # Verifica propriedades básicas
            assert modelo_arquivo.nome == caminho_existente.name
            assert isinstance(modelo_arquivo.tamanho_bytes, int)
            assert modelo_arquivo.tamanho_bytes >= 0

            # Verifica datas de modificação/criação
            assert modelo_arquivo.data_modificacao is not None
            assert modelo_arquivo.data_criacao is not None
            assert isinstance(modelo_arquivo.data_modificacao, datetime)
            assert isinstance(modelo_arquivo.data_criacao, datetime)

    def test_criar_modelo_com_caminho_inexistente(self) -> None:
        """Deve criar modelo com valores default quando o caminho não existe."""
        caminho_inexistente = Path("/caminho/invalido/arquivo.txt")
        modelo_invalido = CaminhoBase(caminho=caminho_inexistente)

        # Propriedades devem refletir que o arquivo não existe
        assert Path(str(modelo_invalido.caminho)).name == "arquivo.txt"
        assert modelo_invalido.nome is None  # Nome só é extraído se caminho existe
        assert modelo_invalido.tamanho_bytes == 0
        assert modelo_invalido.data_modificacao is None
        assert modelo_invalido.data_criacao is None

    def test_modelo_possui_todos_atributos_esperados(self) -> None:
        """Verifica se o modelo contém todos os atributos necessários."""
        with tempfile.TemporaryDirectory() as diretorio_temporario:
            # Cria arquivo de teste
            arquivo_teste = Path(diretorio_temporario) / "documento.txt"
            arquivo_teste.write_text("conteúdo de teste")

            # Cria pasta de teste
            pasta_teste = Path(diretorio_temporario) / "subpasta"
            pasta_teste.mkdir()

            # Testa ambos os cenários
            elementos_teste = [arquivo_teste, pasta_teste]

            for caminho_elemento in elementos_teste:
                modelo_elemento = CaminhoBase(caminho=caminho_elemento)

                atributos_obrigatorios = [
                    "caminho",
                    "nome",
                    "tamanho_bytes",
                    "data_modificacao",
                    "data_criacao",
                    "oculto",
                    "extensao",
                    "pai",
                ]

                # Verifica existência de todos os atributos
                for atributo in atributos_obrigatorios:
                    assert hasattr(modelo_elemento, atributo)

                # Validações específicas por tipo
                if caminho_elemento.is_file():
                    assert modelo_elemento.tamanho_bytes is not None
                    assert modelo_elemento.tamanho_bytes > 0
                    assert modelo_elemento.extensao == ".txt"
                else:
                    # Pastas não têm extensão
                    assert modelo_elemento.extensao in (None, "")

    def test_detectar_arquivo_oculto(self) -> None:
        """Deve identificar corretamente arquivos ocultos (que começam com .)."""
        with tempfile.TemporaryDirectory() as diretorio_temporario:
            # Arquivo normal (não oculto)
            arquivo_normal = Path(diretorio_temporario) / "visivel.txt"
            arquivo_normal.touch()
            modelo_normal = CaminhoBase(caminho=arquivo_normal)
            assert modelo_normal.oculto is False

            # Arquivo oculto (começa com ponto)
            arquivo_oculto = Path(diretorio_temporario) / ".config"
            arquivo_oculto.touch()
            modelo_oculto = CaminhoBase(caminho=arquivo_oculto)
            assert modelo_oculto.oculto is True

    def test_obter_caminho_pai(self) -> None:
        """Deve retornar o diretório pai do caminho atual."""
        with tempfile.NamedTemporaryFile() as arquivo_temporario:
            caminho_arquivo = Path(arquivo_temporario.name)
            modelo_arquivo = CaminhoBase(caminho=caminho_arquivo)
            assert modelo_arquivo.pai is not None
            assert Path(modelo_arquivo.pai) == caminho_arquivo.parent


# CORREÇÃO 1: Renomear a fixture para um nome único que não conflite
@pytest.fixture
def fixture_arquivo_temp() -> Generator[Path, None, None]:
    """
    Fixture que cria um arquivo temporário único para testes.
    O arquivo é removido automaticamente após o teste.
    """
    with tempfile.NamedTemporaryFile(delete=False) as arquivo_temp:
        arquivo_temp.write(b"conteudo de teste")
        arquivo_temp.flush()
        caminho_arquivo = Path(arquivo_temp.name)
        yield caminho_arquivo
    # Limpeza após o teste
    os.unlink(caminho_arquivo)


def test_modelo_com_fixture_de_arquivo(fixture_arquivo_temp: Path) -> None:
    """Testa criação de modelo utilizando a fixture de arquivo temporário."""
    modelo = CaminhoBase(caminho=fixture_arquivo_temp)

    assert modelo.tamanho_bytes is not None
    assert modelo.tamanho_bytes > 0
    assert modelo.nome == fixture_arquivo_temp.name


def test_listar_conteudo_e_buscar_por_nome_em_diretorio() -> None:
    """Testa as funcionalidades de listagem e busca em um diretório."""
    with tempfile.TemporaryDirectory() as diretorio_temporario:
        diretorio = Path(diretorio_temporario)

        # Cria estrutura de teste
        arquivo_a = diretorio / "documentoA.txt"
        arquivo_b = diretorio / "Relatorio.doc"
        subpasta = diretorio / "arquivos_antigos"

        arquivo_a.write_text("linha1\nlinha2")
        arquivo_b.write_text("conteudo do relatorio")
        subpasta.mkdir()

        # Testa listagem simples
        modelo_diretorio = CaminhoBase(caminho=diretorio)
        itens_listados = modelo_diretorio.listar_conteudo_simples()
        nomes_encontrados = {item["nome"] for item in itens_listados}

        assert "documentoA.txt" in nomes_encontrados
        assert "Relatorio.doc" in nomes_encontrados
        assert "arquivos_antigos" in nomes_encontrados

        # Testa busca por nome (case insensitive)
        resultados_busca = modelo_diretorio.buscar_por_nome("documento")
        assert any(r["nome"] == "documentoA.txt" for r in resultados_busca)

        resultados_case_insensitive = modelo_diretorio.buscar_por_nome("RELATORIO")
        assert any(r["nome"] == "Relatorio.doc" for r in resultados_case_insensitive)

        # Verifica se caminho_completo está presente nos resultados
        for item in resultados_busca + resultados_case_insensitive:
            caminho_completo_str = item["caminho_completo"]
            assert isinstance(caminho_completo_str, str)
            caminho_completo = Path(caminho_completo_str)
            assert str(caminho_completo.parent) == str(diretorio)


# CORREÇÃO 2: Adicionar type hint para tmp_path
def test_mudar_caminho_e_recarregar_propriedades(tmp_path: Path) -> None:
    """Testa a funcionalidade de mudar o caminho e recarregar dados."""
    caminho_inexistente = tmp_path / "arquivo_inexistente.txt"
    modelo = CaminhoBase(caminho=caminho_inexistente)
    assert modelo.existe is False

    # Cria arquivo e muda o caminho do modelo para ele
    arquivo_real = tmp_path / "arquivo_real.txt"
    arquivo_real.write_text("conteudo")

    # CORREÇÃO 3: Converter Path para str explicitamente
    mudou_com_sucesso = modelo.mudar_caminho(str(arquivo_real))
    assert mudou_com_sucesso is True
    assert modelo.existe is True
    assert modelo.nome == arquivo_real.name

    # Tenta mudar para caminho inexistente novamente
    mudou_com_falha = modelo.mudar_caminho(str(caminho_inexistente))
    assert mudou_com_falha is False
    assert modelo.existe is False


def test_contar_linhas_em_arquivo_texto(tmp_path: Path) -> None:
    """Testa a contagem de linhas para arquivos de texto."""
    arquivo = tmp_path / "multilinhas.txt"
    conteudo = "primeira linha\nsegunda linha\nterceira linha\n"
    arquivo.write_text(conteudo, encoding="utf-8")

    modelo = CaminhoBase(caminho=arquivo)
    assert modelo.linhas == conteudo.count("\n")

    # CORREÇÃO 4: info_completa é método, info_detalhada é propriedade
    # Verificar se ambos retornam o mesmo tipo de dado
    info_completa_result = modelo.info_completa()
    info_detalhada_result = modelo.info_detalhada
    assert info_completa_result == info_detalhada_result


def test_propriedade_is_pasta_diferencia_arquivos_de_diretorios(tmp_path: Path) -> None:
    """Verifica se a propriedade is_pasta funciona corretamente."""
    diretorio = tmp_path / "minha_pasta"
    diretorio.mkdir()

    arquivo = tmp_path / "meu_arquivo.txt"
    arquivo.write_text("x")

    modelo_diretorio = CaminhoBase(caminho=diretorio)
    modelo_arquivo = CaminhoBase(caminho=arquivo)

    assert modelo_diretorio.is_pasta is True
    assert modelo_arquivo.is_pasta is False


def test_listar_conteudo_em_arquivo_retorna_vazio(tmp_path: Path) -> None:
    """Listar conteúdo em um arquivo deve retornar lista vazia."""
    arquivo = tmp_path / "arquivo.txt"
    arquivo.write_text("conteudo")

    modelo = CaminhoBase(caminho=arquivo)
    assert len(modelo.listar_conteudo_simples()) == 0


def test_buscar_por_nome_em_arquivo_retorna_vazio(tmp_path: Path) -> None:
    """Buscar por nome em um arquivo deve retornar lista vazia (não é diretório)."""
    arquivo = tmp_path / "documento.txt"
    arquivo.write_text("conteudo")

    modelo = CaminhoBase(caminho=arquivo)
    assert len(modelo.buscar_por_nome("documento")) == 0


def test_listagem_inclui_tamanho_apenas_para_arquivos(tmp_path: Path) -> None:
    """Na listagem, o campo 'tamanho' deve aparecer apenas para arquivos."""
    diretorio = tmp_path / "diretorio_teste"
    diretorio.mkdir()

    arquivo = diretorio / "dados.txt"
    arquivo.write_text("12345")

    subpasta = diretorio / "subdiretorio"
    subpasta.mkdir()

    modelo = CaminhoBase(caminho=diretorio)
    itens_listados = modelo.listar_conteudo_simples()

    itens_por_nome = {item["nome"]: item for item in itens_listados}
    assert "dados.txt" in itens_por_nome
    assert "subdiretorio" in itens_por_nome

    # Arquivo deve ter campo tamanho
    assert "tamanho" in itens_por_nome["dados.txt"]
    # Diretório NÃO deve ter campo tamanho
    assert "tamanho" not in itens_por_nome["subdiretorio"]


def test_tamanho_total_soma_tamanhos_de_arquivos_no_diretorio(tmp_path: Path) -> None:
    """O tamanho_total deve somar corretamente os bytes de todos arquivos no diretório."""
    diretorio = tmp_path / "pasta_com_arquivos"
    diretorio.mkdir()

    arquivo_pequeno = diretorio / "pequeno.bin"
    arquivo_medio = diretorio / "medio.bin"

    arquivo_pequeno.write_bytes(b"abc")  # 3 bytes
    arquivo_medio.write_bytes(b"12345")  # 5 bytes

    modelo = CaminhoBase(caminho=diretorio)
    assert modelo.tamanho_total == 8  # 3 + 5
    assert modelo.tamanho_bytes == 8


def test_contar_linhas_com_encoding_latin1(tmp_path: Path) -> None:
    """Testa contagem de linhas em arquivo com encoding Latin-1 (ISO-8859-1)."""
    arquivo = tmp_path / "latin1.txt"
    conteudo = "çá\né\n"
    arquivo.write_text(conteudo, encoding="latin-1")

    modelo = CaminhoBase(caminho=arquivo)
    assert modelo.linhas == conteudo.count("\n")


def test_info_detalhada_contem_todas_chaves_obrigatorias(tmp_path: Path) -> None:
    """O dicionário retornado por info_detalhada deve conter todas as chaves esperadas."""
    arquivo = tmp_path / "informacoes.txt"
    arquivo.write_text("dados")

    modelo = CaminhoBase(caminho=arquivo)
    info_completa = modelo.info_detalhada

    chaves_esperadas = {"caminho", "nome", "tipo", "existe", "tamanho_bytes", "extensao", "pai", "itens"}
    assert chaves_esperadas.issubset(set(info_completa.keys()))


def test_recarregar_atualiza_tamanho_apos_modificacao(tmp_path: Path) -> None:
    """Recarregar deve atualizar o tamanho_bytes após o arquivo ser modificado."""
    arquivo = tmp_path / "modificado.txt"
    arquivo.write_text("conteudo inicial")

    modelo = CaminhoBase(caminho=arquivo)
    tamanho_inicial = modelo.tamanho_bytes

    # Modifica o arquivo (aumenta tamanho)
    novo_conteudo = "conteudo inicial" + "x" * 100
    arquivo.write_text(novo_conteudo)

    # Sem recarregar, o tamanho ainda é o antigo
    assert modelo.tamanho_bytes == tamanho_inicial

    # Após recarregar, o tamanho deve ser atualizado
    modelo.recarregar()
    if tamanho_inicial is not None:
        assert modelo.tamanho_bytes is not None
        assert modelo.tamanho_bytes > tamanho_inicial


### **1. Teste para propriedades faltantes**
def test_propriedades_adicionais_sao_carregadas(tmp_path: Path) -> None:
    """Testa se propriedades como permissoes, dono e mime_type são carregadas."""
    arquivo = tmp_path / "teste.txt"
    arquivo.write_text("conteudo")

    modelo = CaminhoBase(caminho=arquivo)

    # Verifica propriedades não testadas
    assert modelo.permissoes is not None
    assert len(modelo.permissoes) == 3  # formato octal
    assert modelo.dono is not None
    assert modelo.mime_type is not None
    assert modelo.mime_type.startswith("text/")


### **2. Teste para quantidade_itens**


def test_quantidade_itens_em_pasta(tmp_path: Path) -> None:
    """Testa se quantidade_itens conta corretamente."""
    pasta = tmp_path / "minha_pasta"
    pasta.mkdir()

    # Cria 3 arquivos
    for i in range(3):
        (pasta / f"arquivo{i}.txt").write_text("teste")

    modelo = CaminhoBase(caminho=pasta)
    assert modelo.quantidade_itens == 3
    assert len(modelo.itens) == 3


### **3. Teste para data_acesso**


def test_data_acesso_e_preenchida(tmp_path: Path) -> None:
    """Testa se data_acesso é preenchida (pode ser igual à modificação)."""
    arquivo = tmp_path / "acesso.txt"
    arquivo.write_text("teste")

    modelo = CaminhoBase(caminho=arquivo)
    assert modelo.data_acesso is not None
    assert isinstance(modelo.data_acesso, datetime)


### **4. Teste para tratamento de erros**


def test_carregar_propriedades_com_erro_permissao(monkeypatch, tmp_path: Path) -> None:
    """Testa comportamento quando há erro de permissão."""
    arquivo = tmp_path / "sem_permissao.txt"
    arquivo.write_text("teste")

    # Salva o estado original do modelo
    modelo = CaminhoBase(caminho=arquivo)
    assert modelo._erro is None  # Inicialmente sem erro

    # Simula erro de permissão no stat APÓS criar o modelo
    def mock_stat(*args, **kwargs):
        raise PermissionError("Permissão negada")

    monkeypatch.setattr(Path, "stat", mock_stat)

    # Recarrega para forçar o erro
    modelo.recarregar()

    # Verifica se o erro foi capturado
    assert modelo._erro is not None
    assert "Permissão" in modelo._erro or "permissão" in modelo._erro.lower()

    # Propriedades devem ter valores padrão
    assert modelo.tamanho_bytes == 0
    assert modelo.data_criacao is None


### **5. Teste para validar_caminho**


def test_validar_caminho_com_entradas_variadas() -> None:
    """Testa o validador de caminho com diferentes entradas."""

    # Testa com string vazia (deve lançar erro)
    with pytest.raises(ValueError):
        CaminhoBase(caminho="")

    # Testa com None (deve lançar erro)
    with pytest.raises(ValueError):
        CaminhoBase(caminho=None)  # type: ignore

    # Testa com Path object
    caminho_path = Path("/home/teste")
    modelo = CaminhoBase(caminho=caminho_path)
    assert modelo.caminho == str(caminho_path.expanduser().resolve(strict=False))


### **6. Teste para carregar_propriedades_arquivo com tipos especiais**


def test_carregar_arquivo_nao_texto(tmp_path: Path) -> None:
    """Testa carregamento de arquivo binário (não texto)."""
    arquivo = tmp_path / "dados.bin"
    arquivo.write_bytes(b"\x00\x01\x02\x03")

    modelo = CaminhoBase(caminho=arquivo)
    assert modelo.linhas is None  # Não deve contar linhas
    assert modelo.mime_type is not None
