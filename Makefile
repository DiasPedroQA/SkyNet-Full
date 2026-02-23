# ===================================
# SkyNet - Makefile
# ===================================

SHELL := /bin/bash

# Diretórios
BACKEND_DIR := backend
FRONTEND_DIR := frontend

.PHONY: help setup dev backend frontend build up \
        test coverage lint format clean lint-frontend format-frontend

# ===================================
# Help
# ===================================
help:
	@echo ""
	@echo "🚀 SkyNet - Comandos disponíveis:"
	@echo ""
	@echo "  📦 Setup"
	@echo "    make setup         - Instala dependências do backend e frontend"
	@echo ""
	@echo "  🚀 Desenvolvimento"
	@echo "    make dev           - Inicia backend + frontend (modo desenvolvimento)"
	@echo "    make backend       - Inicia apenas o backend"
	@echo "    make frontend      - Inicia apenas o frontend"
	@echo ""
	@echo "  🏭 Produção"
	@echo "    make build         - Build do frontend para produção"
	@echo "    make up            - Inicia backend em modo produção"
	@echo ""
	@echo "  🧪 Testes"
	@echo "    make test          - Executa testes do backend"
	@echo "    make test-frontend - Executa testes do frontend"
	@echo "    make coverage      - Gera relatório de cobertura"
	@echo ""
	@echo "  🔧 Qualidade"
	@echo "    make lint          - Verifica código backend e frontend"
	@echo "    make lint-backend  - Verifica apenas backend (com config)"
	@echo "    make lint-frontend - Verifica apenas frontend"
	@echo "    make format        - Formata código backend e frontend"
	@echo "    make format-backend - Formata apenas backend (com config)"
	@echo "    make format-frontend - Formata apenas frontend"
	@echo ""
	@echo "  🧹 Limpeza"
	@echo "    make clean         - Remove arquivos temporários"
	@echo ""

# ===================================
# Setup
# ===================================
setup:
	@echo "🐍 Configurando backend..."
	cd $(BACKEND_DIR) && python -m venv .venv
	cd $(BACKEND_DIR) && .venv/bin/pip install --upgrade pip
	cd $(BACKEND_DIR) && .venv/bin/pip install -r requirements.txt
	@echo "⚛️  Configurando frontend..."
	cd $(FRONTEND_DIR) && npm install
	@echo "✅ Setup concluído!"

# ===================================
# Desenvolvimento
# ===================================
dev:
	@echo "🔥 Iniciando backend e frontend..."
	@trap 'echo "🛑 Encerrando..."; kill 0' SIGINT; \
	cd $(BACKEND_DIR) && .venv/bin/uvicorn app.main:app --reload & \
	cd $(FRONTEND_DIR) && npm run dev & \
	wait

backend:
	@echo "🐍 Iniciando backend..."
	cd $(BACKEND_DIR) && .venv/bin/uvicorn app.main:app --reload

frontend:
	@echo "⚛️ Iniciando frontend..."
	cd $(FRONTEND_DIR) && npm run dev

# ===================================
# Produção
# ===================================
build:
	@echo "🏗️  Build do frontend..."
	cd $(FRONTEND_DIR) && npm run build

up:
	@echo "🚀 Iniciando backend em produção..."
	cd $(BACKEND_DIR) && .venv/bin/uvicorn app.main:app

# ===================================
# Testes
# ===================================
test:
	@echo "🧪 Testando backend..."
	cd $(BACKEND_DIR) && .venv/bin/pytest

test-frontend:
	@echo "🧪 Testando frontend..."
	cd $(FRONTEND_DIR) && npm test

coverage:
	@echo "📊 Gerando relatório de cobertura..."
	cd $(BACKEND_DIR) && .venv/bin/pytest --cov=app --cov-report=term-missing --cov-report=html
	@echo "📁 Relatório HTML gerado em $(BACKEND_DIR)/htmlcov/"

# ===================================
# Qualidade - Backend (com configuração explícita)
# ===================================
lint-backend:
	@echo "🔍 Verificando código backend com configuração..."
	cd $(BACKEND_DIR) && .venv/bin/ruff check . --config pyproject.toml

format-backend:
	@echo "✨ Formatando código backend com configuração..."
	cd $(BACKEND_DIR) && .venv/bin/ruff check . --config pyproject.toml --fix

# ===================================
# Qualidade - Frontend
# ===================================
lint-frontend:
	@echo "🔍 Verificando código frontend..."
	@cd $(FRONTEND_DIR) && npm run lint 2>/dev/null || echo "⚠️  Lint do frontend não configurado (crie um script 'lint' no package.json)"

format-frontend:
	@echo "✨ Formatando código frontend..."
	@cd $(FRONTEND_DIR) && npm run format 2>/dev/null || echo "⚠️  Format do frontend não configurado (crie um script 'format' no package.json)"

# ===================================
# Qualidade - Combinados
# ===================================
lint: lint-backend lint-frontend

format: format-backend format-frontend

# ===================================
# Limpeza
# ===================================
clean:
	@echo "🧹 Removendo arquivos temporários..."
	rm -rf \
		$(BACKEND_DIR)/.pytest_cache \
		$(BACKEND_DIR)/__pycache__ \
		$(BACKEND_DIR)/htmlcov \
		$(BACKEND_DIR)/.coverage \
		$(BACKEND_DIR)/.ruff_cache \
		$(FRONTEND_DIR)/dist \
		$(FRONTEND_DIR)/.vite \
		$(FRONTEND_DIR)/node_modules/.vite \
		$(FRONTEND_DIR)/coverage \
		$(FRONTEND_DIR)/.eslintcache
	@echo "✅ Limpeza concluída!"

# ===================================
# Utilitários
# ===================================
ruff-version:
	@echo "🐍 Versão do Ruff:"
	@cd $(BACKEND_DIR) && .venv/bin/ruff --version

ruff-show-config:
	@echo "🔧 Configuração do Ruff:"
	@cd $(BACKEND_DIR) && .venv/bin/ruff check . --show-settings | grep -E "line-length|config"

check-ruff-config:
	@echo "🔍 Verificando se o Ruff está lendo a configuração correta..."
	@cd $(BACKEND_DIR) && .venv/bin/ruff check . --config pyproject.toml --no-cache | head -10 || echo "✅ Nenhum erro encontrado!"
