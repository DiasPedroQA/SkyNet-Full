// frontend/types/user.types.ts
/**
 * TYPES: Definem a estrutura dos dados no frontend
 * Garantem type safety em toda a aplicação
 */

export interface User {
  id: number;
  username: string;
  email: string;
  created_at: string;
}

export interface UserLoginRequest {
  email: string;
  password: string;
}

export interface UserRegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  message: string;
  user: User;
}
