import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1'; // URL base da API

// Função para obter a lista de favoritos
export const getFavorites = async () => {
    try {
        const response = await axios.get(`${API_URL}/favorites`);
        return response.data;
    } catch (error) {
        console.error('Erro ao obter favoritos:', error);
        throw error;
    }
};

// Função para adicionar um novo favorito
export const addFavorite = async (favorite) => {
    try {
        const response = await axios.post(`${API_URL}/favorites`, favorite);
        return response.data;
    } catch (error) {
        console.error('Erro ao adicionar favorito:', error);
        throw error;
    }
};

// Função para atualizar um favorito existente
export const updateFavorite = async (id, favorite) => {
    try {
        const response = await axios.put(`${API_URL}/favorites/${id}`, favorite);
        return response.data;
    } catch (error) {
        console.error('Erro ao atualizar favorito:', error);
        throw error;
    }
};

// Função para deletar um favorito
export const deleteFavorite = async (id) => {
    try {
        await axios.delete(`${API_URL}/favorites/${id}`);
    } catch (error) {
        console.error('Erro ao deletar favorito:', error);
        throw error;
    }
};