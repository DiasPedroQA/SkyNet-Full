import React, { useEffect, useState } from 'react';
import { getFavorites } from '../services/api';

const FavoriteList: React.FC = () => {
    const [favorites, setFavorites] = useState([]);

    useEffect(() => {
        const fetchFavorites = async () => {
            const data = await getFavorites();
            setFavorites(data);
        };

        fetchFavorites();
    }, []);

    return (
        <div>
            <h2>Lista de Favoritos</h2>
            <ul>
                {favorites.map((favorite) => (
                    <li key={favorite.id}>
                        <a href={favorite.url} target="_blank" rel="noopener noreferrer">
                            {favorite.title}
                        </a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default FavoriteList;