"""
System Builder Module.

Este módulo define a classe responsável por construir e orquestrar
as entidades internas do domínio relacionadas ao sistema operacional
e à sessão de usuário.

O SystemBuilder atua como uma camada de montagem (Factory/Façade),
sendo o único ponto público autorizado a instanciar os modelos
internos `_OperatingSystem` e `_UserSession`.

Responsabilidades:
- Detectar informações do ambiente de execução
- Criar instâncias imutáveis das entidades de domínio
- Expor uma estrutura padronizada pronta para serialização
"""

import getpass
import os
import platform
import socket
from pathlib import Path
from typing import Any, Self

from ._models import _OperatingSystem, _UserSession


class SystemBuilder:
    """
    Classe responsável por construir e fornecer a representação
    consolidada do sistema e da sessão ativa.

    Esta classe encapsula a lógica de criação das entidades internas
    do domínio, impedindo que sejam instanciadas diretamente fora
    desta camada.

    O builder atua como:
    - Factory para os modelos internos
    - Façade para exposição do modelo consolidado
    """

    def __init__(
        self,
        os_model: _OperatingSystem,
        session: _UserSession,
    ) -> None:
        """
        Inicializa o builder com as entidades de domínio já construídas.

        Args:
            os_model (_OperatingSystem):
                Instância representando o sistema operacional.

            session (_UserSession):
                Instância representando a sessão ativa do usuário.
        """
        self.__os: _OperatingSystem = os_model
        self.__session: _UserSession = session

    @classmethod
    def build_from_environment(cls) -> Self:
        """
        Constrói uma instância de SystemBuilder a partir do ambiente atual.

        Este método detecta automaticamente informações do sistema
        operacional e da sessão ativa utilizando módulos padrão
        da biblioteca do Python.

        Returns:
            Self:
                Instância totalmente configurada de SystemBuilder
                com os dados do ambiente atual.
        """

        os_model = _OperatingSystem(
            name=platform.system(),
            version=platform.release(),
            root_path=str(Path("/").anchor),
            path_separator=os.sep,
            case_sensitive=True,
        )

        hostname: str = socket.gethostname()

        session = _UserSession(
            username=getpass.getuser(),
            home_directory=str(Path.home()),
            current_directory=os.getcwd(),
            hostname=hostname,
            ip_address=socket.gethostbyname(hostname),
        )

        return cls(os_model, session)

    def to_dict(self) -> dict[str, Any]:
        """
        Retorna a estrutura final consolidada do sistema.

        A saída segue o formato padronizado definido pelo domínio:

        {
            "system": {
                "os": {...}
            },
            "session": {...}
        }

        Returns:
            dict:
                Estrutura serializável representando o sistema
                operacional e a sessão ativa.
        """

        return {
            "system": {"os": self.__os.model_dump()},
            "session": self.__session.model_dump(),
        }
