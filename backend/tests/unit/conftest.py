"""Fixtures compartilhadas para todos os testes. Configurações de teste para o pytest."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.database import get_db
from app.infrastructure.models.favorite import Base
from app.main import app


@pytest.fixture
def client():
    """Fixture que fornece um cliente de teste com banco em memória."""
    # Banco em memória para testes
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def override_settings(monkeypatch):
    """Sobrescreve configurações para usar SQLite durante os testes."""
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./test_skynet.db")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("ENVIRONMENT", "testing")

    settings.database_url = "sqlite:///./test_skynet.db"
