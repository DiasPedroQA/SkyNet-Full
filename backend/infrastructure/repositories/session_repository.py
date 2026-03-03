"""Módulo do UserSession"""

from sqlite3 import Connection, Cursor

from models._models import _UserSession


class UserSessionRepository:
    """
    Repositório responsável pela persistência de UserSession.
    """

    def __init__(self, connection: Connection) -> None:
        """Inicializa a classe"""
        self._conn: Connection = connection

    def save(self, session: _UserSession) -> None:
        """Faz as inserções no banco com a tabela do User"""
        cursor: Cursor = self._conn.cursor()

        cursor.execute(
            """
            INSERT INTO user_session (
                username, home_directory, current_directory,
                hostname, ip_address
            ) VALUES (?, ?, ?, ?, ?)
        """,
            (
                session.username,
                session.home_directory,
                session.current_directory,
                session.hostname,
                session.ip_address,
            ),
        )

        self._conn.commit()
