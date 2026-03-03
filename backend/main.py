"""
Main da aplicação.

- Mantém a estrutura de inicialização do FastAPI (comentada)
- Permite testar Model isoladamente
- Permite testar Repository isoladamente
"""

from pprint import pprint
from sqlite3 import Connection

from models.builder import SystemBuilder
from infrastructure.database import DatabaseConnection
from infrastructure.repositories.os_repository import OperatingSystemRepository
from infrastructure.repositories.session_repository import UserSessionRepository


# =============================================================================
# TESTES LOCAIS (MODEL + REPOSITORY)
# =============================================================================

if __name__ == "__main__":
    print("\n==============================")
    print("🔎 TESTE 1 — Model puro")
    print("==============================\n")

    # -------------------------------------------------------------------------
    # Teste do Model isolado
    # -------------------------------------------------------------------------

    # Builder cria o domínio
    system_builder: SystemBuilder = SystemBuilder.build_from_environment()

    # Banco
    db = DatabaseConnection()
    conn: Connection = db.connect()

    # Repositórios
    os_repo = OperatingSystemRepository(conn)
    session_repo = UserSessionRepository(conn)

    # Persistindo
    os_repo.save(system_builder._SystemBuilder__os)
    session_repo.save(system_builder._SystemBuilder__session)

    print("Dados persistidos com sucesso.")

    pprint(system_builder.to_dict())

    # -------------------------------------------------------------------------
    # Teste do Repository isolado
    # -------------------------------------------------------------------------

    # print("\n==============================")
    # print("🔎 TESTE 2 — Repository com SQLite temporário")
    # print("==============================")

    # test_db_path = Path(settings.DATABASE_URL)

    # CRIAR_TABELA_SYSTEM = """
    # CREATE TABLE IF NOT EXISTS system (
    #     name TEXT,
    #     version TEXT,
    #     environment TEXT,
    #     uptime_seconds INTEGER,
    #     status TEXT
    # )
    # """
    # DELETAR_TABELA_SYSTEM = "DELETE FROM system"
    # INSERIR_NA_TABELA_SYSTEM = """
    # INSERT INTO system (name, version, environment, uptime_seconds, status)
    # VALUES (?, ?, ?, ?, ?)
    # """

    # CRIAR_TABELA_USERS = """
    # CREATE TABLE IF NOT EXISTS users (
    #     id INTEGER PRIMARY KEY,
    #     username TEXT,
    #     role TEXT,
    #     is_active INTEGER,
    #     email TEXT,
    #     last_login TEXT
    # )
    # """
    # DELETAR_TABELA_USERS = "DELETE FROM users"
    # INSERIR_NA_TABELA_USERS = """
    # INSERT INTO users (username, role, is_active, email, last_login)
    # VALUES (?, ?, ?, ?, ?)
    # """

    # with sqlite3.connect(test_db_path) as conn:
    #     conn.execute(CRIAR_TABELA_SYSTEM)
    #     conn.execute(CRIAR_TABELA_USERS)

    #     conn.execute(DELETAR_TABELA_SYSTEM)
    #     conn.execute(DELETAR_TABELA_USERS)

    #     conn.execute(
    #         INSERIR_NA_TABELA_SYSTEM,
    #         (settings.APP_NAME, settings.APP_VERSION, settings.ENVIRONMENT, 5400, "running"),
    #     )

    #     conn.execute(
    #         INSERIR_NA_TABELA_USERS,
    #         (
    #             "pedro",
    #             "admin",
    #             1,
    #             "pedro@email.com",
    #             datetime.now().isoformat(),
    #         ),
    #     )

    #     conn.commit()

    # # Instancia repository apontando para banco de teste
    # repo = SystemRepository(db_path=test_db_path)

    # system_info_repo: EstadoSistema = repo.get_system_info(user_id=1)

    # print("📦 Resultado do Repository:")
    # print(system_info_repo.to_dict())

    # # Limpeza
    # test_db_path.unlink(missing_ok=True)

    print("\n✅ Testes finalizados com sucesso.\n")


# from repositories.user_repository import SystemRepository

# =============================================================================
# INICIALIZAÇÃO FASTAPI (MANTIDA, MAS NÃO EXECUTADA AGORA)
# =============================================================================

# import uvicorn
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from controllers.system_controller import router as system_router
# from config import settings


# def create_application() -> FastAPI:
#     """Cria e configura a aplicação FastAPI."""
#
#     app = FastAPI(
#         title=settings.APP_NAME,
#         version=settings.APP_VERSION,
#         debug=settings.API_DEBUG,
#     )
#
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=["*"],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )
#
#     app.include_router(system_router)
#
#     return app
#
#
# application: FastAPI = create_application()
#
#
# if __name__ == "__main__":
#     uvicorn.run(
#         "backend.main:application",
#         host=settings.API_HOST,
#         port=settings.API_PORT,
#         reload=settings.API_RELOAD,
#     )


# """
# Sistema SkyNet-Mobile - API FastAPI com utilitários de sistema de arquivos
# Ponto de entrada unificado da aplicação com ferramentas de teste e demonstração
# """

# import argparse
# from pathlib import Path
# from pprint import pprint

# import uvicorn

# ============================================================================
# IMPORTAÇÕES DA API FASTAPI
# ============================================================================
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from app.core.config import settings

# Importa router v1 de forma segura (se o pacote estiver incompleto evita crash)
# try:
#     from app.interfaces.api.v1 import router as V1_ROUTER

#     _HAS_V1_ROUTER = True
# except (ImportError, ModuleNotFoundError):
#     V1_ROUTER = None
#     _HAS_V1_ROUTER = False

# ============================================================================
# IMPORTAÇÕES DO SISTEMA DE ARQUIVOS
# ============================================================================
# try:
#     from models import ArquivoInfo, PastaInfo
#     from services.formatadores import formatar_tamanho

#     _HAS_FS_MODELS = True
# except (ImportError, ModuleNotFoundError):
#     ArquivoInfo = PastaInfo = None
#     formatar_tamanho = lambda x: f"{x} bytes"
#     _HAS_FS_MODELS = False

# ============================================================================
# CONFIGURAÇÃO DA APLICAÇÃO FASTAPI
# ============================================================================
# app: FastAPI = FastAPI(
#     title=settings.app_name,
#     description="API para gerenciamento de favoritos do SkyNet-Mobile com utilitários de sistema de arquivos",
#     version="0.1.0",
#     debug=settings.debug,
#     docs_url="/docs" if settings.debug else None,
#     redoc_url="/redoc" if settings.debug else None,
# )

# ============================================================================
# MIDDLEWARE CORS
# ============================================================================
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.allowed_origins_list,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# ============================================================================
# ROTAS DA API
# ============================================================================
# if _HAS_V1_ROUTER and V1_ROUTER is not None:
#     app.include_router(V1_ROUTER, prefix=settings.api_v1_prefix)


# ============================================================================
# ENDPOINTS DE SAÚDE E INFORMAÇÕES
# ============================================================================
# @app.get("/")
# async def root() -> dict[str, str | bool | int]:
#     """Endpoint raiz para verificar se a API está rodando."""
#     return {
#         "message": "🚀 Bem-vindo à SkyNet-Mobile API!",
#         "app": settings.app_name,
#         "version": "0.1.0",
#         "docs": "/docs" if settings.debug else "Disponível apenas em desenvolvimento",
#         "health": "/health",
#         "fs_tools": "/fs-demo" if _HAS_FS_MODELS else "Módulo de arquivos não disponível",
#     }


# @app.get("/health")
# async def health_check() -> dict[str, str | bool]:
#     """Endpoint para verificar a saúde da aplicação."""
#     return {
#         "status": "healthy",
#         "app": settings.app_name,
#         "debug": settings.debug,
#         "database": "sqlite" if "sqlite" in settings.database_url else "postgresql",
#         "fs_models": "disponível" if _HAS_FS_MODELS else "indisponível",
#     }


# @app.get("/info")
# async def info() -> dict[str, str | bool | list[str]]:
#     """Endpoint para retornar informações básicas da aplicação."""
#     return {
#         "app_name": settings.app_name,
#         "version": "0.1.0",
#         "debug": settings.debug,
#         "api_prefix": settings.api_v1_prefix,
#         "cors_origins": settings.allowed_origins_list,
#         "environment": "development" if settings.debug else "production",
#         "fs_tools_available": _HAS_FS_MODELS,
#     }


# ============================================================================
# ENDPOINTS DO SISTEMA DE ARQUIVOS (apenas se os modelos estiverem disponíveis)
# ============================================================================
# if _HAS_FS_MODELS:

#     class CaminhoFactory:
#         """
#         Fábrica para criar objetos do sistema de arquivos.
#         Auto-detecta o tipo do caminho e retorna a classe apropriada.
#         """

#         @staticmethod
#         def ler_caminho(caminho_input: str | Path, **kwargs) -> ArquivoInfo | PastaInfo:
#             """Cria e retorna a instância apropriada based no tipo do caminho."""
#             caminho_obj = Path(caminho_input).expanduser().absolute()
#             caminho_str = str(caminho_obj)

#             if not caminho_obj.exists():
#                 raise ValueError(f"O caminho '{caminho_input}' não existe")

#             if caminho_obj.is_file():
#                 return ArquivoInfo(caminho=caminho_str, **kwargs)
#             if caminho_obj.is_dir():
#                 return PastaInfo(caminho=caminho_str, **kwargs)

#             raise TypeError(f"Tipo de caminho não suportado: {caminho_input}")

#         @staticmethod
#         def ler_caminho_seguro(caminho_input: str | Path, **kwargs) -> ArquivoInfo | PastaInfo | None:
#             """Versão segura que não levanta exceções."""
#             try:
#                 return CaminhoFactory.ler_caminho(caminho_input, **kwargs)
#             except (ValueError, TypeError, OSError, PermissionError):
#                 return None

#         @staticmethod
#         def identificar_tipo_caminho(caminho_input: str | Path) -> str:
#             """Identifica o tipo do caminho sem criar o objeto completo."""
#             try:
#                 caminho_obj = Path(caminho_input).expanduser().absolute()

#                 if not caminho_obj.exists():
#                     return "inexistente"
#                 if caminho_obj.is_file():
#                     return "arquivo"
#                 if caminho_obj.is_dir():
#                     return "pasta"
#                 return "desconhecido"
#             except (OSError, PermissionError):
#                 return "erro"

#     @app.get("/fs/info/{caminho:path}")
#     async def fs_info(caminho: str):
#         """Endpoint para obter informações de um arquivo ou pasta."""
#         try:
#             caminho_obj: Path = Path(caminho).expanduser().absolute()

#             if not caminho_obj.exists():
#                 return {"erro": "Caminho não existe", "caminho": str(caminho_obj)}

#             if caminho_obj.is_file():
#                 arquivo = ArquivoInfo(caminho=str(caminho_obj))
#                 return {
#                     "tipo": "arquivo",
#                     "nome": arquivo.nome,
#                     "tamanho": formatar_tamanho(arquivo.tamanho_bytes or 0),
#                     "tamanho_bytes": arquivo.tamanho_bytes,
#                     "extensao": arquivo.extensao,
#                     "oculto": arquivo.oculto,
#                     "permissoes": arquivo.permissoes,
#                     "dono": arquivo.dono,
#                     "criacao": arquivo.data_criacao.isoformat() if arquivo.data_criacao else None,
#                     "modificacao": arquivo.data_modificacao.isoformat() if arquivo.data_modificacao else None,
#                     "mime_type": arquivo.mime_type,
#                 }
#             else:
#                 pasta = PastaInfo(caminho=str(caminho_obj))
#                 return {
#                     "tipo": "pasta",
#                     "nome": pasta.nome,
#                     "quantidade_itens": pasta.quantidade_itens,
#                     "tamanho_total": formatar_tamanho(pasta.tamanho_total or 0),
#                     "permissoes": pasta.permissoes,
#                     "dono": pasta.dono,
#                     "itens_preview": pasta.itens[:10] if pasta.itens else [],
#                 }
#         except Exception as e:
#             return {"erro": str(e), "caminho": caminho}

#     @app.get("/fs/check")
#     async def fs_check():
#         """Endpoint para verificar se o módulo de arquivos está funcionando."""
#         return {
#             "status": "ok",
#             "models_disponiveis": True,
#             "exemplos": {
#                 "arquivo": "/fs/info/" + __file__,
#                 "pasta": "/fs/info/.",
#             },
#         }

# ============================================================================
# SISTEMA DE TESTES E DEMONSTRAÇÕES (apenas para execução direta)
# ============================================================================


# class DemonstradorSistemaArquivos:
#     """Classe responsável por demonstrar o uso dos modelos do sistema de arquivos"""

#     def __init__(self, modo_interativo: bool = False):
#         self.modo_interativo = modo_interativo
#         self.factory = CaminhoFactory if _HAS_FS_MODELS else None

#     def _cabecalho(self, titulo: str, largura: int = 70, character: str = "=") -> None:
#         """Exibe um cabeçalho formatado"""
#         print()
#         print(character * largura)
#         print(titulo.center(largura))
#         print(character * largura)

#     def _print_status(self, icone: str, mensagem: str, nivel: int = 1) -> None:
#         """Imprime uma mensagem com ícone de status e indentação"""
#         indentacao = "  " * nivel
#         print(f"{indentacao}{icone} {mensagem}")

#     def _pausar_se_interativo(self) -> None:
#         """Pausa a execução se estiver em modo interativo"""
#         if self.modo_interativo:
#             input("\n    Pressione Enter para continuar...")

#     def demonstrar_api(self) -> None:
#         """Demonstra os endpoints da API disponíveis"""
#         self._cabecalho("🌐 DEMONSTRAÇÃO DA API FASTAPI")

#         self._print_status("📡", "Endpoints disponíveis:")
#         print("    • Root:        /")
#         print("    • Health:      /health")
#         print("    • Info:        /info")
#         if _HAS_FS_MODELS:
#             print("    • FS Check:    /fs/check")
#             print(f"    • FS Info:     /fs/info/{Path(__file__).name}")

#         self._print_status("🚀", f"Para iniciar o servidor: uvicorn {Path(__file__).stem}:app --reload")
#         self._pausar_se_interativo()

#     def demonstrar_factory(self) -> None:
#         """Demonstração do uso do CaminhoFactory"""
#         if not _HAS_FS_MODELS:
#             print("❌ Modelos de sistema de arquivos não disponíveis")
#             return

#         self._cabecalho("🏭 DEMONSTRAÇÃO DO CAMINHOFACTORY")

#         # Cenário 1: Arquivo existente
#         self._print_status("📄", "1. CRIANDO ARQUIVO EXISTENTE:")
#         try:
#             arquivo = CaminhoFactory.ler_caminho(__file__)
#             self._print_status("✓", f"Nome: {arquivo.nome}", 2)
#             self._print_status("📊", f"Tamanho: {formatar_tamanho(arquivo.tamanho_bytes or 0)}", 2)
#             self._print_status("🔤", f"Extensão: {arquivo.extensao}", 2)
#         except Exception as e:
#             self._print_status("✗", f"Erro: {e}", 2)

#         # Cenário 2: Pasta existente
#         self._print_status("📁", "2. CRIANDO PASTA EXISTENTE:")
#         try:
#             pasta = CaminhoFactory.ler_caminho(".")
#             self._print_status("✓", f"Nome: {pasta.nome}", 2)
#             self._print_status("🔢", f"Itens: {pasta.quantidade_itens}", 2)
#         except Exception as e:
#             self._print_status("✗", f"Erro: {e}", 2)

#         self._pausar_se_interativo()


# def criar_parser() -> argparse.ArgumentParser:
#     """Cria o parser de argumentos da linha de comando"""
#     parser = argparse.ArgumentParser(
#         description="SkyNet-Mobile - API com utilitários de sistema de arquivos",
#         formatter_class=argparse.RawDescriptionHelpFormatter,
#         epilog="""
#         Exemplos de uso:
#             python run.py --serve              # Inicia o servidor API
#             python run.py --demo-api           # Demonstra endpoints da API
#             python run.py --demo-factory       # Demonstra o CaminhoFactory
#             python run.py --menu                # Menu interativo completo
#             python run.py --caminho ~/arquivo   # Analisa um caminho específico
#         """,
#     )

#     parser.add_argument("--serve", action="store_true", help="Inicia o servidor FastAPI")

#     parser.add_argument("--caminho", nargs="?", help="Caminho específico para analisar")

#     parser.add_argument("--demo-api", action="store_true", help="Demonstra os endpoints da API")

#     parser.add_argument("--demo-factory", action="store_true", help="Demonstra o CaminhoFactory")

#     parser.add_argument("--menu", action="store_true", help="Menu interativo")

#     parser.add_argument("--host", default="0.0.0.0", help="Host do servidor (padrão: 0.0.0.0)")

#     parser.add_argument("--port", type=int, default=8000, help="Porta do servidor (padrão: 8000)")

#     return parser


# def menu_interativo() -> None:
#     """Menu interativo para o usuário"""
#     demo = DemonstradorSistemaArquivos(modo_interativo=True)

#     while True:
#         print("\n" + "=" * 70)
#         print("🚀 SKYNET-MOBILE - SISTEMA UNIFICADO".center(70))
#         print("=" * 70)
#         print("\nEscolha uma opção:")
#         print("  1. 🌐 Iniciar servidor API")
#         print("  2. 📡 Demonstrar endpoints da API")
#         print("  3. 🏭 Demonstrar CaminhoFactory")
#         print("  4. 🔍 Analisar caminho específico")
#         print("  5. 📊 Verificar saúde do sistema")
#         print("  0. Sair")

#         opcao: str = input("\nOpção: ").strip()

#         if opcao == "1":
#             print("\n🚀 Iniciando servidor... Pressione Ctrl+C para parar")
#             uvicorn.run(
#                 f"{Path(__file__).stem}:app",
#                 host="0.0.0.0",
#                 port=8000,
#                 reload=settings.debug,
#             )

#         elif opcao == "2":
#             demo.demonstrar_api()

#         elif opcao == "3":
#             demo.demonstrar_factory()

#         elif opcao == "4":
#             caminho = input("Caminho para analisar: ").strip()
#             if caminho and _HAS_FS_MODELS:
#                 tipo = CaminhoFactory.identificar_tipo_caminho(caminho)
#                 print(f"\n📌 Tipo detectado: {tipo}")

#                 if tipo in ["arquivo", "pasta"]:
#                     obj = CaminhoFactory.ler_caminho_seguro(caminho)
#                     if obj:
#                         print("\n📋 Informações:")
#                         for chave, valor in obj.info_completa().items():
#                             if chave != "itens":
#                                 print(f"    • {chave}: {valor}")
#             else:
#                 print("❌ Módulo de arquivos não disponível")

#         elif opcao == "5":
#             print("\n📊 SAÚDE DO SISTEMA:")
#             print("    • API FastAPI: ✅ disponível")
#             print(f"    • Models Arquivos: {'✅ disponível' if _HAS_FS_MODELS else '❌ indisponível'}")
#             print(f"    • Router V1: {'✅ disponível' if _HAS_V1_ROUTER else '❌ indisponível'}")
#             print(f"    • Debug: {settings.debug}")

#         elif opcao == "0":
#             print("\n👋 Até mais!")
#             break

#         else:
#             print("❌ Opção inválida!")


# def analisar_caminho(caminho: str) -> None:
#     """Analisa um caminho específico"""
#     if not _HAS_FS_MODELS:
#         print("❌ Modelos de sistema de arquivos não disponíveis")
#         return

#     print(f"\n🔍 Analisando: {caminho}")
#     tipo = CaminhoFactory.identificar_tipo_caminho(caminho)
#     print(f"📌 Tipo: {tipo}")

#     if tipo in ["arquivo", "pasta"]:
#         obj = CaminhoFactory.ler_caminho_seguro(caminho)
#         if obj:
#             print("\n📋 INFORMAÇÕES COMPLETAS:")
#             pprint(obj.info_completa())
#     else:
#         print("❌ Caminho inválido ou inacessível")


# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================


# def main() -> None:
#     """Função principal unificada"""
#     parser = criar_parser()
#     args = parser.parse_args()

#     if args.serve:
#         print(f"🚀 Iniciando {settings.app_name}...")
#         uvicorn.run(
#             f"{Path(__file__).stem}:app",
#             host=args.host,
#             port=args.port,
#             reload=settings.debug,
#             log_level="debug" if settings.debug else "info",
#         )

#     elif args.menu:
#         menu_interativo()

#     elif args.caminho:
#         analisar_caminho(args.caminho)

#     elif args.demo_api:
#         DemonstradorSistemaArquivos().demonstrar_api()

#     elif args.demo_factory:
#         DemonstradorSistemaArquivos().demonstrar_factory()

#     else:
#         parser.print_help()


# if __name__ == "__main__":
#     main()

# from pprint import pprint
# from sqlite3 import Connection

# from models.builder import SystemBuilder
# from infrastructure.database import DatabaseConnection
# from infrastructure.repositories.os_repository import OperatingSystemRepository
# from infrastructure.repositories.session_repository import UserSessionRepository


# =============================================================================
# TESTES LOCAIS (MODEL + REPOSITORY)
# =============================================================================

# if __name__ == "__main__":
#     print("\n==============================")
#     print("🔎 TESTE 1 — Model puro")
#     print("==============================\n")

#     # -------------------------------------------------------------------------
#     # Teste do Model isolado
#     # -------------------------------------------------------------------------

#     # Builder cria o domínio
#     system_builder: SystemBuilder = SystemBuilder.build_from_environment()

#     # Banco
#     db = DatabaseConnection()
#     conn: Connection = db.connect()

#     # Repositórios
#     os_repo = OperatingSystemRepository(conn)
#     session_repo = UserSessionRepository(conn)

#     # Persistindo
#     os_repo.save(system_builder._SystemBuilder__os)
#     session_repo.save(system_builder._SystemBuilder__session)

#     print("Dados persistidos com sucesso.")

#     pprint(system_builder.to_dict())

#     # -------------------------------------------------------------------------
#     # Teste do Repository isolado
#     # -------------------------------------------------------------------------

#     # print("\n==============================")
#     # print("🔎 TESTE 2 — Repository com SQLite temporário")
#     # print("==============================")

#     # test_db_path = Path(settings.DATABASE_URL)

#     # CRIAR_TABELA_SYSTEM = """
#     # CREATE TABLE IF NOT EXISTS system (
#     #     name TEXT,
#     #     version TEXT,
#     #     environment TEXT,
#     #     uptime_seconds INTEGER,
#     #     status TEXT
#     # )
#     # """
#     # DELETAR_TABELA_SYSTEM = "DELETE FROM system"
#     # INSERIR_NA_TABELA_SYSTEM = """
#     # INSERT INTO system (name, version, environment, uptime_seconds, status)
#     # VALUES (?, ?, ?, ?, ?)
#     # """

#     # CRIAR_TABELA_USERS = """
#     # CREATE TABLE IF NOT EXISTS users (
#     #     id INTEGER PRIMARY KEY,
#     #     username TEXT,
#     #     role TEXT,
#     #     is_active INTEGER,
#     #     email TEXT,
#     #     last_login TEXT
#     # )
#     # """
#     # DELETAR_TABELA_USERS = "DELETE FROM users"
#     # INSERIR_NA_TABELA_USERS = """
#     # INSERT INTO users (username, role, is_active, email, last_login)
#     # VALUES (?, ?, ?, ?, ?)
#     # """

#     # with sqlite3.connect(test_db_path) as conn:
#     #     conn.execute(CRIAR_TABELA_SYSTEM)
#     #     conn.execute(CRIAR_TABELA_USERS)

#     #     conn.execute(DELETAR_TABELA_SYSTEM)
#     #     conn.execute(DELETAR_TABELA_USERS)

#     #     conn.execute(
#     #         INSERIR_NA_TABELA_SYSTEM,
#     #         (settings.APP_NAME, settings.APP_VERSION, settings.ENVIRONMENT, 5400, "running"),
#     #     )

#     #     conn.execute(
#     #         INSERIR_NA_TABELA_USERS,
#     #         (
#     #             "pedro",
#     #             "admin",
#     #             1,
#     #             "pedro@email.com",
#     #             datetime.now().isoformat(),
#     #         ),
#     #     )

#     #     conn.commit()

#     # # Instancia repository apontando para banco de teste
#     # repo = SystemRepository(db_path=test_db_path)

#     # system_info_repo: EstadoSistema = repo.get_system_info(user_id=1)

#     # print("📦 Resultado do Repository:")
#     # print(system_info_repo.to_dict())

#     # # Limpeza
#     # test_db_path.unlink(missing_ok=True)

#     print("\n✅ Testes finalizados com sucesso.\n")


# from repositories.user_repository import SystemRepository

# =============================================================================
# INICIALIZAÇÃO FASTAPI (MANTIDA, MAS NÃO EXECUTADA AGORA)
# =============================================================================

# import uvicorn
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from controllers.system_controller import router as system_router
# from config import settings


# def create_application() -> FastAPI:
#     """Cria e configura a aplicação FastAPI."""
#
#     app = FastAPI(
#         title=settings.APP_NAME,
#         version=settings.APP_VERSION,
#         debug=settings.API_DEBUG,
#     )
#
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=["*"],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )
#
#     app.include_router(system_router)
#
#     return app
#
#
# application: FastAPI = create_application()
#
#
# if __name__ == "__main__":
#     uvicorn.run(
#         "backend.main:application",
#         host=settings.API_HOST,
#         port=settings.API_PORT,
#         reload=settings.API_RELOAD,
#     )
