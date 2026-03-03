"""
Módulo responsável pela inicialização e gerenciamento da conexão
com o banco de dados SQLite da aplicação.

Este módulo encapsula:

    - Criação automática do arquivo de banco (caso não exista)
    - Criação das tabelas necessárias
    - Fornecimento de conexões sob demanda
    - Isolamento da camada de infraestrutura

A classe aqui definida atua como ponto de entrada da persistência
relacional baseada em SQLite.
"""

import sqlite3


class DatabaseConnection:
    """
    Gerencia a conexão com o banco de dados SQLite.

    Responsabilidades:
        - Garantir que o banco de dados exista
        - Criar as tabelas necessárias na inicialização
        - Fornecer conexões para uso pelos repositórios

    Esta classe pertence à camada de infraestrutura e não deve
    conter regras de negócio.
    """

    def __init__(self, db_path: str = "./database_system.db") -> None:
        """
        Inicializa o gerenciador de banco de dados.

        Args:
            db_path (str): Caminho para o arquivo do banco SQLite.
            Caso o arquivo não exista, ele será criado.

        Side Effects:
            - Cria o arquivo do banco (se necessário)
            - Executa a criação das tabelas
        """
        self._db_path: str = db_path
        self._initialize()

    def _initialize(self) -> None:
        """
        Cria as tabelas da aplicação caso ainda não existam.

        Tabelas criadas:
            - operating_system
            - user_session

        Esta operação é idempotente, pois utiliza
        `CREATE TABLE IF NOT EXISTS`.
        """
        with sqlite3.connect(self._db_path) as conn:
            cursor: sqlite3.Cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS operating_system (
                    operating_system_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    version TEXT NOT NULL,
                    root_path TEXT NOT NULL,
                    path_separator TEXT NOT NULL,
                    case_sensitive INTEGER NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_session (
                    user_session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    home_directory TEXT NOT NULL,
                    current_directory TEXT NOT NULL,
                    hostname TEXT NOT NULL,
                    ip_address TEXT NOT NULL
                )
            """)

            conn.commit()

    def connect(self) -> sqlite3.Connection:
        """
        Cria e retorna uma nova conexão com o banco de dados.

        Returns:
            sqlite3.Connection: Objeto de conexão ativo.

        Observações:
            - Cada chamada retorna uma nova conexão.
            - O chamador é responsável por fechar a conexão.
            - Ideal para uso dentro de repositórios ou context managers.
        """
        return sqlite3.connect(self._db_path)
