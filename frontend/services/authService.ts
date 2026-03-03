// frontend/services/authService.ts
import { apiService } from './api';
import { User, UserLoginRequest, UserRegisterRequest, AuthResponse } from '../types/user.types';

class AuthService {
  async login(credentials: UserLoginRequest): Promise<User> {
    const response: AuthResponse = await apiService.post<AuthResponse>('/users/login', credentials);

    // Salva dados do usuário (você pode salvar um token JWT)
    localStorage.setItem('user', JSON.stringify(response.user));

    return response.user;
  }

  async register(userData: UserRegisterRequest): Promise<User> {
    const response: AuthResponse = await apiService.post<AuthResponse>('/users/register', userData);
    return response.user;
  }

  async logout(): Promise<void> {
    localStorage.removeItem('user');
    // Opcional: chamar endpoint de logout
  }

  getCurrentUser(): User | null {
    const userStr: string | null = localStorage.getItem('user');
    if (userStr) {
      return JSON.parse(userStr);
    }
    return null;
  }

  isAuthenticated(): boolean {
    return !!this.getCurrentUser();
  }
}

export const authService = new AuthService();
