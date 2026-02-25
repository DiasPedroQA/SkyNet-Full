"""Engine e Session para SQLAlchemy e função get_db para dependência FastAPI."""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# Configura engine; para sqlite precisamos do check_same_thread
_engine_kwargs: dict[str, dict[str, bool]] = (
    {"connect_args": {"check_same_thread": False}} if "sqlite" in settings.database_url else {}
)
engine = create_engine(settings.database_url, **_engine_kwargs)

# Session factory reutilizável
SessionLocal: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa compartilhada para modelos SQLAlchemy
Base = declarative_base()


def get_db() -> Generator:
    """
    Dependency para endpoints FastAPI.
    Gera uma sessão e garante fechamento ao final da request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
