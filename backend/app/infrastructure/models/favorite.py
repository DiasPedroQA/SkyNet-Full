"""Módulo de compatibilidade para imports antigos que esperam app.models.favorite.Base."""

# Exporta Base do core.database para compatibilidade com testes/fixtures.
from app.core.database import Base

__all__ = ["Base"]
