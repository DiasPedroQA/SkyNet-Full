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
