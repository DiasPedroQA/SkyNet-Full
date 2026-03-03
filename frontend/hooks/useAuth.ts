// frontend/hooks/useAuth.ts
/**
 * HOOKS: Lógica reutilizável com React
 * Encapsulam estado e efeitos
 */

import { useState, useEffect, useCallback } from 'react';
import { authService } from '../services/authService';
import { User, UserLoginRequest, UserRegisterRequest } from '../types/user.types';

export const useAuth: () => {user: User|null; loading: boolean; error: string|null} = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Verifica usuário logado ao montar o componente
    const currentUser: User | null = authService.getCurrentUser();
    setUser(currentUser);
    setLoading(false);
  }, []);

  const login: (credentials: UserLoginRequest) => Promise<User> = useCallback(async (credentials: UserLoginRequest) => {
    setLoading(true);
    setError(null);

    try {
      const user = await authService.login(credentials);
      setUser(user);
      return user;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao fazer login');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const register: (userData: UserRegisterRequest) => Promise<User> = useCallback(async (userData: UserRegisterRequest) => {
    setLoading(true);
    setError(null);

    try {
      const user = await authService.register(userData);
      return user;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao registrar');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout: () => Promise<void> = useCallback(async () => {
    await authService.logout();
    setUser(null);
  }, []);

  return {
    user,
    loading,
    error,
    login,
    register,
    logout,
    isAuthenticated: !!user
  };
};
