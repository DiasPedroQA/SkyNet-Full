# """Módulo de teste unitário para o serviço de favoritos"""

# import pytest
# from fastapi import HTTPException

# from app.services.favorite_service import FavoriteService


# def test_create_favorite():
#     """Teste para verificar a criação de um novo favorito"""
#     service = FavoriteService()
#     favorite_data = {"name": "Test Favorite", "url": "http://example.com"}
#     favorite = service.create_favorite(favorite_data)

#     assert favorite.name == favorite_data["name"]
#     assert favorite.url == favorite_data["url"]

# def test_get_favorite():
#     """Teste para verificar a obtenção de um favorito pelo ID"""
#     service = FavoriteService()
#     favorite_data = {"name": "Test Favorite", "url": "http://example.com"}
#     created_favorite = service.create_favorite(favorite_data)

#     favorite = service.get_favorite(created_favorite.id)

#     assert favorite.id == created_favorite.id
#     assert favorite.name == created_favorite.name

# def test_update_favorite():
#     """Teste para verificar a atualização de um favorito existente"""
#     service = FavoriteService()
#     favorite_data = {"name": "Test Favorite", "url": "http://example.com"}
#     created_favorite = service.create_favorite(favorite_data)

#     updated_data = {"name": "Updated Favorite", "url": "http://example.org"}
#     updated_favorite = service.update_favorite(created_favorite.id, updated_data)

#     assert updated_favorite.name == updated_data["name"]
#     assert updated_favorite.url == updated_data["url"]

# def test_delete_favorite():
#     """Teste para verificar a exclusão de um favorito"""
#     service = FavoriteService()
#     favorite_data = {"name": "Test Favorite", "url": "http://example.com"}
#     created_favorite = service.create_favorite(favorite_data)

#     service.delete_favorite(created_favorite.id)

#     with pytest.raises(HTTPException):
#         service.get_favorite(created_favorite.id)
