# SkyNet Backend 🐍

Backend da aplicação SkyNet-Mobile, construído com FastAPI para gerenciamento de favoritos.

## 🚀 Tecnologias

- **FastAPI** - Framework web de alta performance
- **SQLAlchemy** - ORM para banco de dados
- **Pydantic** - Validação de dados
- **Ruff** - Linter e formatador
- **Pytest** - Testes automatizados

## 📁 Estrutura do Projeto

```text
backend/
├── app/
│   ├── api/               # Rotas da API (inclui schemas)
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   └── favorites.py   # Rotas + schemas de favoritos
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py      # Configurações da aplicação
│   │   └── database.py    # Configuração do banco de dados
│   ├── models/
│   │   ├── __init__.py
│   │   └── favorite.py    # Modelo + repositório de favoritos
│   ├── services/
│   │   ├── __init__.py
│   │   └── favorite_service.py # Lógica de negócio
│   ├── __init__.py
│   └── main.py            # Ponto de entrada da aplicação
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # Fixtures para testes
│   ├── test_api.py        # Testes de API
│   └── test_services.py   # Testes de serviços
├── pyproject.toml         # Configuração do projeto (ruff, pytest)
├── requirements.txt       # Dependências do projeto
└── README.md              # Este arquivo
```

## ⚙️ Configuração Rápida

### 1. Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar (Linux/Mac)
source .venv/bin/activate

# Ativar (Windows)
# .venv\Scripts\activate
```

### 2. Dependências

```bash
# Instalar tudo
pip install -r requirements.txt

# Ou apenas produção
pip install fastapi uvicorn sqlalchemy pydantic
```

### 3. Executar

```bash
# Desenvolvimento (com reload)
uvicorn app.main:app --reload

# Produção
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. Acessar

- API: <http://localhost:8000>
- Docs: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

## 🧪 Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=app --cov-report=term-missing

# Gerar relatório HTML
pytest --cov=app --cov-report=html
```

## 📦 Endpoints da API

|  Método  |           Rota             |         Descrição         |
|----------|----------------------------|---------------------------|
|   GET    |    `/api/v1/favorites`     | Lista todos os favoritos  |
|   GET    |  `/api/v1/favorites/{id}`  |   Busca favorito por ID   |
|   POST   |    `/api/v1/favorites/`    |     Cria novo favorito    |
|  DELETE  |   `/api/v1/favorites/{id}` |      Remove favorito      |
|   GET    |          `/health`         |       Status da API       |

Exemplo de requisição:

```json
POST /api/v1/favorites/
{
  "title": "Google",
  "url": "https://google.com"
}
```

## 🔧 Qualidade de Código

```bash
# Linting
ruff check .

# Formatação automática
ruff check . --fix

# Verificar tipos (opcional)
mypy app
```

## 📝 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do backend:

```env
# App
APP_NAME="SkyNet-Mobile API"
DEBUG=true

# Database
DATABASE_URL="sqlite:///./skynet.db"
```

## 🤝 Como Contribuir

1. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
2. Commit: `git commit -m "feat: adiciona nova funcionalidade"`
3. Push: `git push origin feature/nova-funcionalidade`
4. Abra um Pull Request

## 📄 Licença

GNU © [Dias Pedro](https://github.com/DiasPedroQA)
