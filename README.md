# SkyNet-Mobile

Analisador inteligente de favoritos com arquitetura fullstack moderna, foco em qualidade, testes automatizados e evolução contínua.

---

## 📊 Status do Projeto

![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green)
![React](https://img.shields.io/badge/React-18-blue)
![License](https://img.shields.io/badge/license-GNU-green)

> Projeto estruturado com foco em boas práticas de engenharia de software, arquitetura desacoplada e alta testabilidade.

---

## 🎯 Objetivo

SkyNet-Mobile é uma aplicação fullstack que:

- Processa arquivos HTML de favoritos exportados de navegadores
- Organiza e estrutura links
- Permite CRUD de favoritos
- Prepara dados para análises inteligentes futuras
- Mantém alto padrão arquitetural e de qualidade

---

## 🏗 Arquitetura Geral

```text
SkyNet-Mobile/
├── backend/     → API REST (FastAPI)
├── frontend/    → Interface Web (React + TypeScript)
└── .github/     → CI/CD e automações
````

### Princípios Arquiteturais

- Separação de responsabilidades
- Arquitetura em camadas
- Código desacoplado
- Alta testabilidade
- Preparado para CI/CD

---

## 🐍 Backend

API REST responsável por:

- Gerenciamento de favoritos
- Upload e processamento de HTML
- Regras de negócio
- Persistência em banco de dados

```text
backend/
├── controllers/
├── services/
├── models/
├── infrastructure/
└── tests/
```

📖 Documentação automática disponível em:

- [http://localhost:8000/docs](http://localhost:8000/docs)
- [http://localhost:8000/redoc](http://localhost:8000/redoc)

📌 Documentação técnica detalhada disponível em:

```text
backend/README.md
```

---

## ⚛ Frontend

Interface web responsável por:

- Upload de favoritos
- Visualização e manipulação
- Comunicação com API

```text
frontend/
├── components/
├── pages/
├── services/
├── hooks/
└── tests/
```

---

## 🚀 Início Rápido

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm start
```

---

## 🧪 Testes

### - Backend

```bash
pytest --cov=backend --cov-report=term-missing
```

### - Frontend

```bash
npm test
npm run test:e2e
```

---

## 🔐 Segurança (Roadmap)

- Validação robusta de upload
- Sanitização de HTML
- Análise estática com Bandit
- Verificação de dependências

---

## 📌 Roadmap

- ✔ CRUD de favoritos
- ⏳ Upload completo de HTML
- ⏳ Dashboard com métricas
- ⏳ Autenticação
- ⏳ Deploy
- ⏳ Cobertura mínima obrigatória via CI

---

## 🤝 Contribuição

1. Fork
2. Crie uma branch
3. Commit padronizado
4. Abra um Pull Request

Padrões de commit:

- feat:
- fix:
- docs:
- test:
- refactor:

---

## 👨‍💻 Autor

Dias Pedro
QA Engineer & Backend Developer

---

## 📄 Licença

GNU

````text

---

# 📌 Agora crie separadamente:

## backend/README.md

```md
# SkyNet-Mobile Backend

API REST construída com FastAPI para gerenciamento inteligente de favoritos.

---

## 🏗 Arquitetura

```text
backend/
├── controllers/
├── services/
├── models/
├── infrastructure/
├── schemas/
└── tests/
````

### Camadas

- Controller → Camada HTTP
- Service → Regras de negócio
- Repository → Persistência
- Models → Entidades de domínio

---

## 🚀 Executar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## - 🧪 Testes

```bash
pytest --cov=backend --cov-report=term-missing
```

---

## 🔍 Qualidade

```bash
ruff check .
ruff check . --fix
```

---

## 📝 Variáveis de Ambiente

```ini
APP_NAME="SkyNet-Mobile API"
DATABASE_URL="sqlite:///./skynet.db"
```
