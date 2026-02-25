# pylint: disable=C0114,too-many-instance-attributes, wrong-import-order, import-error,E0401,no-name-in-module
# pyright: reportCallIssue=false
# type: ignore[call-arg]

#!/usr/bin/env python3
# pylint: disable=E0401,R0902,C0114,W0718
# pyright: reportCallIssue=false
# type: ignore[call-arg]

"""
Sistema completo de testes e demonstrações para classes do sistema de arquivos.
Integra Factory Pattern, CLI interativa e demonstrações organizadas.
"""

import argparse
from datetime import datetime
from pathlib import Path
from pprint import pprint
from typing import Sequence

from models import ArquivoInfo, PastaInfo
from services.formatadores import formatar_tamanho

# ============================================================================
# FACTORY - Criação inteligente de objetos
# ============================================================================


class CaminhoFactory:
    """
    Fábrica para criar objetos do sistema de arquivos.
    Auto-detecta o tipo do caminho e retorna a classe apropriada.
    """

    @staticmethod
    def ler_caminho(caminho_input: str | Path, **kwargs) -> ArquivoInfo | PastaInfo:
        """
        Cria e retorna a instância apropriada baseada no tipo do caminho.

        Args:
            caminho_input: String ou objeto Path com o caminho a ser analisado
            **kwargs: Argumentos adicionais para as classes específicas

        Returns:
            Instância de ArquivoInfo ou PastaInfo

        Raises:
            ValueError: Se o caminho não existir
            TypeError: Se o tipo de caminho não for reconhecido
        """
        caminho_obj = Path(caminho_input).expanduser().absolute()
        caminho_str = str(caminho_obj)

        if not caminho_obj.exists():
            raise ValueError(f"O caminho '{caminho_input}' não existe")

        if caminho_obj.is_file():
            return ArquivoInfo(caminho=caminho_str, **kwargs)
        if caminho_obj.is_dir():
            return PastaInfo(caminho=caminho_str, **kwargs)

        raise TypeError(f"Tipo de caminho não suportado: {caminho_input}")

    @staticmethod
    def ler_caminho_seguro(caminho_input: str | Path, **kwargs) -> ArquivoInfo | PastaInfo | None:
        """
        Versão segura que não levanta exceções.

        Args:
            caminho_input: String ou objeto Path com o caminho a ser analisado
            **kwargs: Argumentos adicionais para as classes específicas

        Returns:
            Instância de ArquivoInfo ou PastaInfo, ou None se houver erro
        """
        try:
            return CaminhoFactory.ler_caminho(caminho_input, **kwargs)
        except (ValueError, TypeError, OSError, PermissionError):
            return None

    @staticmethod
    def ler_multiplos_caminhos(caminhos_lista: Sequence[str | Path], **kwargs) -> list[ArquivoInfo | PastaInfo]:
        """
        Cria múltiplos objetos a partir de uma sequência de caminhos.

        Args:
            caminhos_lista: Sequência de caminhos a serem analisados
            **kwargs: Argumentos adicionais para as classes específicas

        Returns:
            Lista com objetos válidos (apenas os que existem)
        """
        objetos_validos = []
        for caminho in caminhos_lista:
            obj = CaminhoFactory.ler_caminho_seguro(caminho, **kwargs)
            if obj and obj.existe:
                objetos_validos.append(obj)
        return objetos_validos

    @staticmethod
    def identificar_tipo_caminho(caminho_input: str | Path) -> str:
        """
        Identifica o tipo do caminho sem criar o objeto completo.

        Args:
            caminho_input: String ou objeto Path com o caminho a ser analisado

        Returns:
            String com o tipo: 'arquivo', 'pasta', 'inexistente' ou 'desconhecido'
        """
        try:
            caminho_obj = Path(caminho_input).expanduser().absolute()

            if not caminho_obj.exists():
                return "inexistente"
            if caminho_obj.is_file():
                return "arquivo"
            if caminho_obj.is_dir():
                return "pasta"
            return "desconhecido"
        except (OSError, PermissionError):
            return "erro"


# Funções auxiliares para compatibilidade
def ler_arquivo(caminho_input: str | Path, **kwargs) -> ArquivoInfo:
    """Função auxiliar para criar especificamente um arquivo."""
    return ArquivoInfo(caminho=str(caminho_input), **kwargs)


def ler_pasta(caminho_input: str | Path, **kwargs) -> PastaInfo:
    """Função auxiliar para criar especificamente uma pasta."""
    return PastaInfo(caminho=str(caminho_input), **kwargs)


def ler_caminho(caminho_input: str | Path, **kwargs) -> ArquivoInfo | PastaInfo:
    """Alias para CaminhoFactory.ler_caminho (compatibilidade)"""
    return CaminhoFactory.ler_caminho(caminho_input, **kwargs)


# ============================================================================
# DEMONSTRADOR - Exibe informações organizadas
# ============================================================================


class DemonstradorSistemaArquivos:
    """Classe responsável por demonstrar o uso dos modelos do sistema de arquivos"""

    def __init__(self, modo_interativo: bool = False):
        self.modo_interativo = modo_interativo
        self.factory = CaminhoFactory()

    def _cabecalho(self, titulo: str, largura: int = 70, caractere: str = "=") -> None:
        """Exibe um cabeçalho formatado"""
        print()
        print(caractere * largura)
        print(titulo.center(largura))
        print(caractere * largura)

    def _print_status(self, icone: str, mensagem: str, nivel: int = 1) -> None:
        """Imprime uma mensagem com ícone de status e indentação"""
        indentacao = "  " * nivel
        print(f"{indentacao}{icone} {mensagem}")

    def _print_info(self, label: str, valor: any, icone: str = "•") -> None:
        """Imprime um par label/valor formatado"""
        print(f"    {icone} {label:<20}: {valor}")

    def _pausar_se_interativo(self) -> None:
        """Pausa a execução se estiver em modo interativo"""
        if self.modo_interativo:
            input("\n    Pressione Enter para continuar...")

    # ========================================================================
    # DEMONSTRAÇÕES ESPECÍFICAS
    # ========================================================================

    def demonstrar_factory(self) -> None:
        """Demonstração completa do uso do CaminhoFactory"""
        self._cabecalho("🏭 DEMONSTRAÇÃO DO CAMINHOFACTORY")

        # Cenário 1: Arquivo existente
        self._print_status("📄", "1. CRIANDO ARQUIVO EXISTENTE:")
        try:
            arquivo = CaminhoFactory.ler_caminho(__file__)
            self._print_info("Nome", arquivo.nome)
            self._print_info("Tipo", arquivo.tipo)
            self._print_info("Tamanho", formatar_tamanho(arquivo.tamanho_bytes or 0))
            self._print_info("Extensão", arquivo.extensao)
        except Exception as e:
            self._print_status("✗", f"Erro: {e}", 2)

        # Cenário 2: Pasta existente
        self._print_status("📁", "2. CRIANDO PASTA EXISTENTE:")
        try:
            pasta = CaminhoFactory.ler_caminho(".")
            self._print_info("Nome", pasta.nome)
            self._print_info("Tipo", pasta.tipo)
            self._print_info("Itens", pasta.quantidade_itens)
            self._print_info("Tamanho total", formatar_tamanho(pasta.tamanho_bytes or 0))
        except Exception as e:
            self._print_status("✗", f"Erro: {e}", 2)

        # Cenário 3: Criação segura
        self._print_status("🔒", "3. CRIAÇÃO SEGURA (CAMINHO INEXISTENTE):")
        resultado = CaminhoFactory.ler_caminho_seguro("/caminho/inexistente")
        if resultado is None:
            self._print_status("✓", "Caminho inexistente tratado corretamente", 2)
        else:
            self._print_status("✗", f"Retornou inesperadamente: {resultado}", 2)

        # Cenário 4: Identificação de tipos
        self._print_status("🔍", "4. IDENTIFICANDO TIPOS DE CAMINHO:")
        caminhos_teste = [__file__, ".", "..", "/caminho/inexistente"]
        for caminho in caminhos_teste:
            tipo = CaminhoFactory.identificar_tipo_caminho(caminho)
            status = "✅" if tipo not in ["inexistente", "erro"] else "❌"
            self._print_status(status, f"{str(caminho):<25} -> {tipo}", 2)

        # Cenário 5: Múltiplos caminhos
        self._print_status("📋", "5. PROCESSANDO MÚLTIPLOS CAMINHOS:")
        objetos = CaminhoFactory.ler_multiplos_caminhos(caminhos_teste)
        self._print_status("✓", f"{len(objetos)} objetos válidos criados", 2)

        self._pausar_se_interativo()

    def demonstrar_arquivo_real(self, caminho: str | None = None) -> None:
        """Demonstra o uso da classe ArquivoInfo com um arquivo real"""
        self._cabecalho("📄 DEMONSTRAÇÃO - ARQUIVOINFO (REAL)")

        caminho_alvo = caminho or __file__
        self._print_status("🎯", f"Analisando: {caminho_alvo}")

        try:
            arquivo = ler_arquivo(caminho_alvo)

            # Informações básicas
            self._print_status("📋", "INFORMAÇÕES BÁSICAS:")
            self._print_info("Nome", arquivo.nome)
            self._print_info("Tipo", arquivo.tipo)
            self._print_info("Extensão", arquivo.extensao)
            self._print_info("Tamanho", formatar_tamanho(arquivo.tamanho_bytes or 0))
            self._print_info("Dono", arquivo.dono)
            self._print_info("Permissões", arquivo.permissoes)
            self._print_info("Oculto", "Sim" if arquivo.oculto else "Não")

            # Verificações
            self._print_status("🔍", "VERIFICAÇÕES:")
            self._print_info("É PDF?", "✅ Sim" if arquivo.eh_pdf() else "❌ Não")
            self._print_info("É imagem?", "✅ Sim" if arquivo.eh_imagem() else "❌ Não")
            self._print_info("É texto?", "✅ Sim" if arquivo.eh_texto() else "❌ Não")

            # Informações adicionais
            self._print_status("📊", "INFORMAÇÕES ADICIONAIS:")
            if arquivo.linhas:
                self._print_info("Linhas", arquivo.linhas)
            self._print_info("MIME type", arquivo.mime_type)

            # Opção de ver detalhes completos
            if self.modo_interativo:
                ver_completo = input("\n    Ver informações completas? (s/N): ").lower()
                if ver_completo == "s":
                    print("\n    📋 INFO COMPLETA:")
                    pprint(arquivo.info_completa())

        except Exception as e:
            self._print_status("❌", f"Erro: {e}")

        self._pausar_se_interativo()

    def demonstrar_pasta_real(self, caminho: str | None = None, recursivo: bool = False) -> None:
        """Demonstra o uso da classe PastaInfo com pastas reais"""
        self._cabecalho("📁 DEMONSTRAÇÃO - PASTAINFO (REAL)")

        caminho_alvo = caminho or "."
        self._print_status("🎯", f"Analisando: {caminho_alvo} (recursivo: {recursivo})")

        try:
            pasta = PastaInfo(caminho=caminho_alvo, incluir_subpastas=recursivo)

            # Informações básicas
            self._print_status("📋", "INFORMAÇÕES BÁSICAS:")
            self._print_info("Nome", pasta.nome)
            self._print_info("Tipo", pasta.tipo)
            self._print_info("Itens totais", pasta.quantidade_itens)
            self._print_info("Arquivos", pasta.contar_arquivos())
            self._print_info("Subpastas", pasta.contar_pastas())
            self._print_info("Tamanho total", formatar_tamanho(pasta.tamanho_total or 0))
            self._print_info("Dono", pasta.dono)
            self._print_info("Permissões", pasta.permissoes)

            # Conteúdo
            self._print_status("📋", "PRIMEIROS 5 ITENS:")
            for _, item in enumerate(pasta.itens[:5], 1):
                icone = "📄" if item.get("tipo") == "arquivo" else "📁"
                self._print_status(icone, f"{item['nome']}", 2)

            if len(pasta.itens) > 5:
                self._print_status("⋯", f"e mais {len(pasta.itens) - 5} itens", 2)

            # Busca por extensão
            if self.modo_interativo:
                ext = input("\n    Filtrar por extensão (ex: .py): ").strip()
                if ext:
                    arquivos = pasta.listar_arquivos_por_extensao(ext)
                    self._print_status("🔍", f"Arquivos .{ext}: {len(arquivos)} encontrados", 2)

        except Exception as e:
            self._print_status("❌", f"Erro: {e}")

        self._pausar_se_interativo()

    def demonstrar_pasta_simulada(self) -> None:
        """Demonstração de manipulação de pastas e arquivos simulados"""
        self._cabecalho("🧪 DEMONSTRAÇÃO - PASTAS SIMULADAS")

        # Criando arquivos simulados
        self._print_status("📄", "1. CRIANDO ARQUIVOS SIMULADOS:")
        agora = datetime.now()

        arquivos = [
            ArquivoInfo(
                caminho="/home/usuario/imagens/foto.jpg",
                nome="foto.jpg",
                tamanho_bytes=2_048_576,  # 2MB
                data_criacao=agora,
                data_modificacao=agora,
                permissoes="644",
                existe=False,
            ),
            ArquivoInfo(
                caminho="/home/usuario/documentos/doc.txt",
                nome="doc.txt",
                tamanho_bytes=1024,  # 1KB
                data_criacao=agora,
                data_modificacao=agora,
                permissoes="644",
                existe=False,
            ),
            ArquivoInfo(
                caminho="/home/usuario/scripts/script.py",
                nome="script.py",
                tamanho_bytes=5120,  # 5KB
                data_criacao=agora,
                data_modificacao=agora,
                permissoes="755",
                existe=False,
            ),
        ]

        for arquivo in arquivos:
            self._print_status("✓", f"{arquivo.nome} ({formatar_tamanho(arquivo.tamanho_bytes or 0)})", 2)

        # Criando pasta
        self._print_status("📁", "2. CRIANDO PASTA SIMULADA:")
        pasta = PastaInfo(
            caminho="/home/usuario",
            nome="Minha Pasta",
            permissoes="755",
            existe=True,
        )
        self._print_status("✓", f"Pasta '{pasta.nome}' criada", 2)

        # Adicionando arquivos
        self._print_status("➕", "3. ADICIONANDO ARQUIVOS À PASTA:")
        for arquivo in arquivos:
            pasta.adicionar_item(arquivo)
        self._print_status("✓", f"Itens na pasta: {pasta.quantidade_itens}", 2)

        # Estatísticas
        self._print_status("📊", "4. ESTATÍSTICAS DA PASTA:")
        self._print_info("Total itens", pasta.quantidade_itens)
        self._print_info("Arquivos", pasta.contar_arquivos())
        self._print_info("Pastas", pasta.contar_pastas())
        self._print_info("Tamanho total", formatar_tamanho(pasta.tamanho_bytes or 0))

        # Buscas
        self._print_status("🔍", "5. BUSCAS:")
        imagens = [i for i in pasta.itens if i.get("extensao") == ".jpg"]
        self._print_info("Imagens JPG", len(imagens))

        encontrado = pasta.encontrar_por_nome("doc.txt")
        if encontrado:
            self._print_info("doc.txt encontrado", "✓")

        self._pausar_se_interativo()


# ============================================================================
# INTERFACE DE LINHA DE COMANDO
# ============================================================================


def criar_parser() -> argparse.ArgumentParser:
    """Cria o parser de argumentos da linha de comando"""
    parser = argparse.ArgumentParser(
        description="Sistema de testes para classes do sistema de arquivos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Exemplos de uso:
            python run_tests.py --menu                   # Menu interativo
            python run_tests.py --tudo                   # Todas as demonstrações
            python run_tests.py arquivo ~/documento.txt  # Testar arquivo específico
            python run_tests.py pasta . --recursivo      # Testar pasta recursivamente
            python run_tests.py --factory                # Apenas demonstração do factory
        """,
    )

    parser.add_argument("caminho", nargs="?", help="Caminho específico para testar")

    parser.add_argument(
        "--tipo",
        choices=["auto", "arquivo", "pasta"],
        default="auto",
        help="Tipo do caminho (auto detecta)",
    )

    parser.add_argument("-r", "--recursivo", action="store_true", help="Incluir subpastas (apenas para pastas)")

    parser.add_argument("--menu", action="store_true", help="Abrir menu interativo")

    parser.add_argument("--factory", action="store_true", help="Executar apenas demonstração do factory")

    parser.add_argument("--arquivo-demo", action="store_true", help="Executar demonstração de arquivo")

    parser.add_argument("--pasta-demo", action="store_true", help="Executar demonstração de pasta real")

    parser.add_argument("--simulada", action="store_true", help="Executar demonstração de pasta simulada")

    parser.add_argument("--tudo", action="store_true", help="Executar todas as demonstrações")

    return parser


def menu_interativo() -> None:
    """Menu interativo para o usuário"""
    demo = DemonstradorSistemaArquivos(modo_interativo=True)

    while True:
        print("\n" + "=" * 70)
        print("🚀 SISTEMA DE TESTES - SKYNET MOBILE".center(70))
        print("=" * 70)
        print("\nEscolha uma opção:")
        print("  1. 📄 Testar arquivo específico")
        print("  2. 📁 Testar pasta específica")
        print("  3. 🏭 Demonstrar CaminhoFactory")
        print("  4. 📄 Demonstrar ArquivoInfo (arquivo atual)")
        print("  5. 📁 Demonstrar PastaInfo (diretório atual)")
        print("  6. 🧪 Demonstrar pasta simulada")
        print("  7. 🔍 Testar caminhos predefinidos")
        print("  8. 🎯 Executar todas as demonstrações")
        print("  0. Sair")

        opcao = input("\nOpção: ").strip()

        if opcao == "1":
            caminho = input("Caminho do arquivo: ").strip()
            if caminho:
                demo.demonstrar_arquivo_real(caminho)

        elif opcao == "2":
            caminho = input("Caminho da pasta: ").strip()
            if caminho:
                recursivo = input("Incluir subpastas? (s/N): ").lower() == "s"
                demo.demonstrar_pasta_real(caminho, recursivo)

        elif opcao == "3":
            demo.demonstrar_factory()

        elif opcao == "4":
            demo.demonstrar_arquivo_real()

        elif opcao == "5":
            demo.demonstrar_pasta_real()

        elif opcao == "6":
            demo.demonstrar_pasta_simulada()

        elif opcao == "7":
            print("\n🔍 TESTANDO CAMINHOS PREDEFINIDOS:")
            demo.demonstrar_arquivo_real(__file__)
            demo.demonstrar_pasta_real(".")

        elif opcao == "8":
            demo.demonstrar_factory()
            demo.demonstrar_arquivo_real()
            demo.demonstrar_pasta_real()
            demo.demonstrar_pasta_simulada()

        elif opcao == "0":
            print("\n👋 Até mais!")
            break

        else:
            print("❌ Opção inválida!")


def testar_caminho_especifico(args) -> None:
    """Testa um caminho específico baseado nos argumentos"""
    demo = DemonstradorSistemaArquivos()

    if args.tipo == "auto":
        tipo = CaminhoFactory.identificar_tipo_caminho(args.caminho)

        if tipo == "arquivo":
            demo.demonstrar_arquivo_real(args.caminho)
        elif tipo == "pasta":
            demo.demonstrar_pasta_real(args.caminho, args.recursivo)
        else:
            print(f"❌ Caminho inválido ou inexistente: {args.caminho}")

    elif args.tipo == "arquivo":
        demo.demonstrar_arquivo_real(args.caminho)

    elif args.tipo == "pasta":
        demo.demonstrar_pasta_real(args.caminho, args.recursivo)


# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================


def main() -> None:
    """Função principal"""
    parser = criar_parser()
    args = parser.parse_args()

    # Prioridade: menu > caminho específico > demonstrações específicas > tudo
    if args.menu:
        menu_interativo()

    elif args.caminho:
        testar_caminho_especifico(args)

    elif args.factory:
        DemonstradorSistemaArquivos().demonstrar_factory()

    elif args.arquivo_demo:
        DemonstradorSistemaArquivos().demonstrar_arquivo_real()

    elif args.pasta_demo:
        DemonstradorSistemaArquivos().demonstrar_pasta_real()

    elif args.simulada:
        DemonstradorSistemaArquivos().demonstrar_pasta_simulada()

    elif args.tudo:
        demo = DemonstradorSistemaArquivos()
        demo.demonstrar_factory()
        demo.demonstrar_arquivo_real()
        demo.demonstrar_pasta_real()
        demo.demonstrar_pasta_simulada()

    else:
        # Se nenhum argumento, mostra ajuda
        parser.print_help()


if __name__ == "__main__":
    main()
