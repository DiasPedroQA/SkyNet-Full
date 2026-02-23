# SkyNet-Mobile

![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.129-green)
![React](https://img.shields.io/badge/React-18-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## Descrição do Projeto

Analisador inteligente de favoritos de navegador

[Início Rápido](#início-rápido) •
[Documentação](#documentação-da-api) •
[Como Contribuir](#guia-de-contribuição)

## Sobre

SkyNet-Mobile é uma aplicação fullstack que processa arquivos HTML de favoritos exportados de navegadores, organizando e permitindo análise dos links salvos pelo usuário.

### Funcionalidades do Sistema

- Upload de arquivos HTML de favoritos
- Processamento automático de links
- Visualização organizada dos favoritos
- Base preparada para futuras análises de padrões

---

## Início Rápido

### Pré-requisitos do Sistema

- Python 3.12 ou superior
- Node.js 18 ou superior
- Docker (opcional)

### Configuração do Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Acesse: <http://localhost:8000>

### Configuração do Frontend

```bash
cd frontend
npm install
npm start
```

Acesse: <http://localhost:3000>

### Execução com Docker

```bash
docker-compose up --build
```

---

## Estrutura do Projeto

```text
SkyNet-Mobile/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── public/
├── .github/
├── docker-compose.yml
└── Makefile
```

---

## Execução de Testes

### Testes do Backend

```bash
cd backend
pytest
pytest -v
pytest --cov=app
```

### Testes do Frontend

```bash
cd frontend
npm test
npm run test:e2e
```

---

## Documentação da API

Com o backend rodando, acesse:

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

### Endpoints Disponíveis

| Método |           Rota           |    Descrição    |
|--------|--------------------------|-----------------|
|  GET   |     /api/v1/favorites    | Lista favoritos |
|  POST  | /api/v1/favorites/upload |   Upload HTML   |
|  GET   |          /health         |  Status da API  |

---

## Tecnologias Utilizadas

### Backend

- FastAPI - Framework web
- Pydantic - Validação de dados
- SQLAlchemy - ORM
- Pytest - Testes

### Frontend

- React - UI Library
- TypeScript - Tipagem estática
- Jest - Testes unitários
- Cypress - Testes E2E

### DevOps

- Docker - Containerização
- GitHub Actions - CI/CD
- Make - Automação

---

## Guia de Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature:

   ```bash
   git checkout -b feature/nova-funcionalidade
   ```

3. Faça commit das suas mudanças:

   ```bash
   git commit -m "feat: adiciona nova funcionalidade"
   ```

4. Faça push para a branch:

   ```bash
   git push origin feature/nova-funcionalidade
   ```

5. Abra um Pull Request

### Padrão de Commits

- feat: - Nova funcionalidade
- fix: - Correção de bug
- docs: - Documentação
- test: - Testes
- refactor: - Refatoração
- style: - Formatação

---

## Roadmap do Projeto

- Concluído: Estrutura base do projeto
- Concluído: CRUD de favoritos
- Pendente: Upload automático de HTML
- Pendente: Dashboard com métricas
- Pendente: Autenticação de usuários
- Pendente: Análise de padrões de navegação
- Pendente: Deploy em produção

---

## Licença

Distribuído sob licença MIT. Veja o arquivo LICENSE para mais informações.

---

## Autor

### **Dias Pedro**

- QA Engineer & Backend Developer
- GitHub: @diaspedro

---

Built with ❤️ by Dias Pedro
