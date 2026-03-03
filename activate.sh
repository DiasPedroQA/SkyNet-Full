#!/bin/bash
# Script para ativar o ambiente virtual do backend

BACKEND_VENV="backend/.SkyNet-Mobile-VENV"

if [ -d "$BACKEND_VENV" ]; then
    echo "✅ Ativando ambiente virtual: $BACKEND_VENV"
    source "$BACKEND_VENV/bin/activate"
    echo "✅ Python: $(which python)"
    echo "✅ Pip: $(which pip)"
    echo ""
    echo "📌 Comandos úteis:"
    echo "   deactivate     # Sair do ambiente virtual"
    echo "   pip list       # Ver pacotes instalados"
    echo "   python backend/main.py  # Rodar a API"
else
    echo "❌ Ambiente virtual não encontrado em: $BACKEND_VENV"
    echo ""
    echo "Para criar:"
    echo "   cd backend"
    echo "   python3 -m venv .SkyNet-Mobile-VENV"
    echo "   source .SkyNet-Mobile-VENV/bin/activate"
    echo "   pip install -r requirements.txt"
fi
