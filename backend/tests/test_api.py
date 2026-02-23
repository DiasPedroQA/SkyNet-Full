"""Testes da API."""


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_favorite(client):
    response = client.post(
        "/api/v1/favorites/", json={"title": "Google", "url": "https://google.com"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Google"
    assert "id" in data
