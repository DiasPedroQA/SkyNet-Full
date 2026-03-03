import sqlite3
from pathlib import Path


class DatabaseConnection:
    """
    Responsável por gerenciar a conexão com o SQLite.
    """

    def __init__(self, db_path: str = "system.db") -> None:
        self._db_path = db_path
        self._initialize()

    def _initialize(self) -> None:
        """
        Cria as tabelas caso não existam.
        """
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS operating_system (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    version TEXT NOT NULL,
                    root_path TEXT NOT NULL,
                    path_separator TEXT NOT NULL,
                    case_sensitive INTEGER NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_session (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    home_directory TEXT NOT NULL,
                    current_directory TEXT NOT NULL,
                    hostname TEXT NOT NULL,
                    ip_address TEXT NOT NULL
                )
            """)

            conn.commit()

    def connect(self):
        return sqlite3.connect(self._db_path)
