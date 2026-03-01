# ===================================
# SkyNet - Makefile (Local Dev Only)
# ===================================

SHELL := /bin/bash

BACKEND := backend
FRONTEND := frontend
VENV := .SkyNet-Mobile-VENV/bin

.PHONY: help setup run dev check test lint format clean reset

# ===================================
# Help
# ===================================
help:
	@echo ""
	@echo "🚀 SkyNet - Comandos principais"
	@echo ""
	@echo "  make setup   -> Instala tudo (backend + frontend)"
	@echo "  make run     -> Setup + lint + test + sobe app"
	@echo "  make dev     -> Sobe backend + frontend"
	@echo "  make check   -> Lint + testes + coverage"
	@echo "  make clean   -> Limpa arquivos temporários"
	@echo "  make reset   -> Limpa tudo e reinstala do zero"
	@echo ""

# ===================================
# Setup
# ===================================
setup:
	@echo "📦 Instalando dependências..."
	cd $(BACKEND) && python -m venv .SkyNet-Mobile-VENV
	cd $(BACKEND) && .SkyNet-Mobile-VENV/bin/pip install --upgrade pip
	cd $(BACKEND) && .SkyNet-Mobile-VENV/bin/pip install -r requirements.txt
	cd $(FRONTEND) && npm install
	@echo "✅ Setup concluído."

# ===================================
# Fluxo Completo
# ===================================
run: check dev

# ===================================
# Desenvolvimento
# ===================================
dev:
	@echo "🔥 Subindo backend + frontend..."
	@trap 'kill 0' SIGINT; \
	cd $(BACKEND) && .SkyNet-Mobile-VENV/bin/uvicorn app.main:app --reload & \
	cd $(FRONTEND) && npm run dev & \
	wait

# ===================================
# Qualidade
# ===================================
check: lint test coverage

lint:
	@echo "🔍 Lint backend..."
	cd $(BACKEND) && $(VENV)/ruff check . --config pyproject.toml
	@echo "🔍 Lint frontend..."
	@cd $(FRONTEND) && npm run lint || echo "⚠️  Frontend sem lint configurado"

format:
	@echo "✨ Formatando backend..."
	cd $(BACKEND) && $(VENV)/ruff check . --fix
	@echo "✨ Formatando frontend..."
	@cd $(FRONTEND) && npm run format || echo "⚠️  Frontend sem format configurado"

test:
	@echo "🧪 Testando backend..."
	cd $(BACKEND) && $(VENV)/pytest
	@echo "🧪 Testando frontend..."
	@cd $(FRONTEND) && npm test || true

coverage:
	@echo "📊 Coverage backend..."
	cd $(BACKEND) && $(VENV)/pytest --cov=app --cov-report=term-missing

# ===================================
# Limpeza
# ===================================
clean:
	@echo "🧹 Limpando arquivos temporários..."
	rm -rf \
		$(BACKEND)/.pytest_cache \
		$(BACKEND)/htmlcov \
		$(BACKEND)/.coverage \
		$(BACKEND)/.ruff_cache \
		$(FRONTEND)/dist \
		$(FRONTEND)/coverage
	@echo "✅ Limpeza concluída."

reset: clean
	rm -rf $(BACKEND)/.SkyNet-Mobile-VENV
	rm -rf $(FRONTEND)/node_modules
	@echo "♻️ Ambiente resetado. Execute 'make setup'"
