import React, { useEffect, useState } from 'react';
import { fetchFavorites } from '../services/api';
import FavoriteList from '../components/FavoriteList';

const Dashboard: React.FC = () => {
    const [favorites, setFavorites] = useState([]);

    useEffect(() => {
        const getFavorites = async () => {
            const data = await fetchFavorites();
            setFavorites(data);
        };

        getFavorites();
    }, []);

    return (
        <div>
            <h1>Dashboard</h1>
            <FavoriteList favorites={favorites} />
        </div>
    );
};

export default Dashboard;