"""Classe responsável por gerenciar as conexões com o banco de dados."""

from sqlite3 import Connection, Cursor

from models._models import _OperatingSystem


class OperatingSystemRepository:
    """
    Repositório responsável pela persistência de OperatingSystem.
    """

    def __init__(self, connection: Connection) -> None:
        """Inicializa a classe de conexão com o banco"""
        self._conn: Connection = connection

    def save(self, os_model: _OperatingSystem) -> None:
        """Faz a inserção de dados no banco"""
        cursor: Cursor = self._conn.cursor()

        cursor.execute(
            """
            INSERT INTO operating_system (
                name, version, root_path, path_separator, case_sensitive
            ) VALUES (?, ?, ?, ?, ?)
        """,
            (
                os_model.name,
                os_model.version,
                os_model.root_path,
                os_model.path_separator,
                int(os_model.case_sensitive),
            ),
        )

        self._conn.commit()
