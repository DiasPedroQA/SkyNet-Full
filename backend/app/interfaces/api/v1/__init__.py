"""Router da API v1 (scaffold mínimo para evitar import-errors)."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["v1"])
async def v1_root() -> dict:
    """Rota raiz da versão 1 para teste rápido da API."""
    return {"message": "API v1 do SkyNet-Mobile disponível"}
