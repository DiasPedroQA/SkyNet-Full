# SkyNet-Mobile

Analisador inteligente de favoritos com arquitetura fullstack, testes automatizados e pipeline de qualidade contínua.

---

## 📊 Status do Projeto

![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.129-green)
![React](https://img.shields.io/badge/React-18-blue)
[![CI](https://github.com/DiasPedroQA/SkyNet-Mobile/actions/workflows/test-multi-os.yml/badge.svg?branch=main)](https://github.com/DiasPedroQA/SkyNet-Mobile/actions)
[![Coverage](https://codecov.io/gh/DiasPedroQA/SkyNet-Mobile/branch/main/graph/badge.svg)](https://codecov.io/gh/DiasPedroQA/SkyNet-Mobile)
![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue)
![License](https://img.shields.io/badge/license-GNU-green)

> 🔬 Projeto estruturado com foco em qualidade, testes automatizados e evolução contínua.

---

## 🎯 Objetivo

SkyNet-Mobile é uma aplicação fullstack que:

* Processa arquivos HTML de favoritos exportados de navegadores
* Organiza e estrutura os links
* Prepara os dados para análises inteligentes futuras
* Mantém alto padrão de qualidade de código

---

## 🧪 Cultura de Qualidade

Inspirado no projeto **test-SO**, o SkyNet-Mobile adota:

* ✔ Testes automatizados no backend e frontend
* ✔ Cobertura de código monitorada
* ✔ Integração contínua via GitHub Actions
* ✔ Separação clara entre camadas (API, Services, Core, Models)
* ✔ Arquitetura desacoplada e testável
* ✔ Pronto para análise estática de segurança (Bandit)
* ✔ Estrutura preparada para cobertura mínima obrigatória

---

## 🏗 Arquitetura

### Backend (FastAPI)

```text
backend/
├── app/
│   ├── api/        → Rotas e controllers
│   ├── core/       → Configurações e utilitários centrais
│   ├── models/     → Modelos de domínio
│   ├── services/   → Regras de negócio
│   └── main.py     → Inicialização da aplicação
└── tests/
```

#### Princípios adotados

* Separação de responsabilidades
* Services independentes de framework
* Testes desacoplados de I/O
* Preparado para expansão de domínio

---

### Frontend (React + TypeScript)

```text
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── public/
```

* Tipagem estática com TypeScript
* Testes unitários com Jest
* Testes E2E com Cypress

---

## 🚀 Início Rápido

### Pré-requisitos

* Python 3.12+
* Node.js 18+
* Docker (opcional)

---

### ▶ Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Acesse: [http://localhost:8000](http://localhost:8000)

---

### ▶ Frontend

```bash
cd frontend
npm install
npm start
```

Acesse: [http://localhost:3000](http://localhost:3000)

---

### 🐳 Execução com Docker

```bash
docker-compose up --build
```

---

## 🧪 Execução de Testes

### Backend

```bash
cd backend
pytest
pytest -v
pytest --cov=app --cov-report=term-missing
```

### Frontend

```bash
cd frontend
npm test
npm run test:e2e
```

---

## 📈 Cobertura de Código

Objetivo arquitetural:

* Cobertura mínima recomendada: **85%+**
* Separação clara entre teste unitário e integração
* Preparado para integração futura com Codecov

---

## 🔐 Segurança

Roadmap de segurança inclui:

* Análise estática com Bandit
* Verificação de dependências
* Validação robusta de upload de arquivos
* Sanitização de HTML recebido

---

## 📡 Documentação da API

Com o backend rodando:

* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Endpoints

| Método |           Rota           |    Descrição    |
| ------ | ------------------------ | --------------- |
| GET    | /api/v1/favorites        | Lista favoritos |
| POST   | /api/v1/favorites/upload | Upload HTML     |
| GET    | /health                  | Status da API   |

---

## 🔄 Pipeline e CI

Projeto preparado para:

* Execução automática de testes
* Validação de cobertura
* Build frontend
* Análise estática
* Docker build

---

## 📌 Roadmap

* ✔ Estrutura base
* ✔ CRUD de favoritos
* ⏳ Upload automático completo
* ⏳ Dashboard com métricas
* ⏳ Autenticação de usuários
* ⏳ Análise de padrões de navegação
* ⏳ Deploy em produção
* ⏳ Cobertura mínima obrigatória via CI
* ⏳ Publicação de métricas públicas

---

## 🤝 Contribuição

1. Fork
2. Branch
3. Commit padronizado
4. Pull Request

### Padrão de Commits

* feat:
* fix:
* docs:
* test:
* refactor:
* style:

---

## 👨‍💻 Author

**Dias Pedro**
QA Engineer & Backend Developer
GitHub: @DiasPedroQA

---

## 📄 Licença

GNU

---
