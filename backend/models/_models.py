"""
Domain Models Module.

Este módulo define os modelos internos (privados) responsáveis por
representar as entidades fundamentais do domínio:

- Sistema Operacional
- Sessão de Usuário

Estas classes são consideradas internas ao domínio e não devem ser
instanciadas diretamente fora da camada de construção (ex: SystemBuilder).

Os modelos utilizam Pydantic para:
- Garantir validação de dados
- Fornecer imutabilidade
- Facilitar serialização
"""

from pydantic import BaseModel, ConfigDict


class _OperatingSystem(BaseModel):
    """
    Modelo interno que representa um Sistema Operacional.

    Esta entidade descreve características essenciais do ambiente
    operacional em execução.

    Attributes:
        name (str):
            Nome do sistema operacional (ex: "Linux", "Windows", "Darwin").

        version (str):
            Versão ou release do sistema operacional.

        root_path (str):
            Caminho raiz do sistema de arquivos.

        path_separator (str):
            Separador padrão de diretórios do sistema ("/" ou "\\").

        case_sensitive (bool):
            Indica se o sistema de arquivos diferencia letras maiúsculas
            e minúsculas nos nomes de arquivos.
    """

    name: str
    version: str
    root_path: str
    path_separator: str
    case_sensitive: bool

    # Torna o modelo imutável após a criação
    model_config: ConfigDict = {
        "frozen": True
    }


class _UserSession(BaseModel):
    """
    Modelo interno que representa a sessão ativa de um usuário.

    Esta entidade encapsula informações relacionadas ao contexto
    atual de execução dentro do sistema.

    Attributes:
        username (str):
            Nome do usuário autenticado na sessão.

        home_directory (str):
            Diretório pessoal (home) do usuário.

        current_directory (str):
            Diretório atual de execução do processo.

        hostname (str):
            Nome da máquina onde a sessão está sendo executada.

        ip_address (str):
            Endereço IP associado ao host atual.
    """

    username: str
    home_directory: str
    current_directory: str
    hostname: str
    ip_address: str

    # Garante que a sessão não possa ser alterada após criada
    model_config: ConfigDict = {
        "frozen": True
    }
